from sqlalchemy.orm import Session
import models
import schemas
from datetime import datetime, timedelta
from typing import List

# =========================
# USER
# =========================
def get_or_create_user(db: Session, email: str, name: str = None, picture: str = None):
    # Inferred from the email pattern rather than requiring the app to send
    # it explicitly — guest accounts are created with
    # "guest_<uuid>@focusbubble.app" (see UserSession.getOrCreateGuestEmail
    # on the Android side), so this needs zero changes there.
    login_type = "guest" if email.endswith("@focusbubble.app") else "google"

    u = db.query(models.User).filter(models.User.email == email).first()
    if u:
        changed = False
        if name and u.name != name:
            u.name = name; changed = True
        if picture and u.picture != picture:
            u.picture = picture; changed = True
        if u.login_type != login_type:
            u.login_type = login_type; changed = True
        if changed:
            u.updated_at = datetime.utcnow()
            db.commit(); db.refresh(u)
        return u
    u = models.User(email=email, name=name, picture=picture, login_type=login_type, updated_at=datetime.utcnow())
    db.add(u); db.commit(); db.refresh(u)
    return u

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def list_users(db: Session):
    return db.query(models.User).all()

def delete_user(db: Session, user_id: int):
    # FocusStats/UserStreak aren't wired into User's cascade relationships in
    # models.py, so they won't be removed automatically by deleting the user
    # row alone — delete them explicitly to avoid orphaned rows.
    db.query(models.FocusStats).filter(models.FocusStats.user_id == user_id).delete()
    db.query(models.UserStreak).filter(models.UserStreak.user_id == user_id).delete()
    user = get_user(db, user_id)
    if user:
        db.delete(user)  # schedules/sessions/block_rules cascade via the User model's own relationships
        db.commit()
        return True
    return False

def deactivate_all_blocks_for_user(db: Session, user_id: int):
    now = datetime.utcnow()
    active = db.query(models.BlockedApp).filter(
        models.BlockedApp.user_id == user_id,
        models.BlockedApp.is_active == True
    ).all()
    for b in active:
        b.is_active = False
        b.end_time = now
    db.commit()

# =========================
# STATS + STREAK
# =========================
def get_or_create_stats(db: Session, user_id: int):
    stats = db.query(models.FocusStats).filter(models.FocusStats.user_id == user_id).first()
    if stats:
        return stats
    stats = models.FocusStats(user_id=user_id)
    db.add(stats); db.commit(); db.refresh(stats)
    return stats

def get_or_create_streak(db: Session, user_id: int):
    streak = db.query(models.UserStreak).filter(models.UserStreak.user_id == user_id).first()
    if streak:
        return streak
    streak = models.UserStreak(user_id=user_id, current_streak=0)
    db.add(streak); db.commit(); db.refresh(streak)
    return streak

def maybe_reset_weekly(stats: models.FocusStats):
    now = datetime.utcnow()
    last = stats.last_week_reset

    if now.isocalendar()[1] != last.isocalendar()[1]:  # new week
        stats.weekly_minutes = 0
        stats.last_week_reset = now

def update_after_session_completion(db: Session, user_id: int, session: models.FocusSession):
    minutes = int((session.end_time - session.start_time).total_seconds() / 60)

    stats = get_or_create_stats(db, user_id)
    streak = get_or_create_streak(db, user_id)

    maybe_reset_weekly(stats)

    stats.all_time_minutes += minutes
    stats.weekly_minutes += minutes
    stats.completed_sessions += 1

    today = datetime.utcnow().date()
    if streak.last_session_date is None:
        streak.current_streak = 1
    else:
        delta = (today - streak.last_session_date.date()).days
        if delta == 1:
            streak.current_streak += 1
        elif delta > 1:
            streak.current_streak = 1

    streak.last_session_date = datetime.utcnow()

    db.commit()
    db.refresh(stats)
    db.refresh(streak)
    return stats, streak

# =========================
# SCHEDULES
# =========================
def create_schedule(db: Session, user_id: int, sched: schemas.ScheduleCreate):
    s = models.Schedule(
        user_id=user_id,
        label=sched.label,
        duration_minutes=sched.duration_minutes,
        apps_csv=",".join(sched.apps),
        is_active=sched.is_active
    )
    db.add(s); db.commit(); db.refresh(s)
    return s

def list_schedules(db: Session, user_id: int):
    rows = db.query(models.Schedule).filter(models.Schedule.user_id == user_id).all()
    out = []
    for r in rows:
        out.append({
            "id": r.id,
            "label": r.label,
            "duration_minutes": r.duration_minutes,
            "apps": r.apps_csv.split(",") if r.apps_csv else [],
            "is_active": r.is_active,
            "created_at": r.created_at
        })
    return out

def delete_schedule(db: Session, user_id: int, schedule_id: int):
    s = db.query(models.Schedule).filter(models.Schedule.user_id == user_id,
                                         models.Schedule.id == schedule_id).first()
    if s:
        db.delete(s); db.commit(); return True
    return False

# =========================
# SESSIONS
# =========================
def start_session(db: Session, user_id: int, schedule_id: int, duration_minutes: int):
    now = datetime.utcnow()
    end = now + timedelta(minutes=duration_minutes)
    s = models.FocusSession(
        user_id=user_id,
        schedule_id=schedule_id,
        start_time=now,
        end_time=end,
        paused=False,
        remaining_seconds=None,
        status="running"
    )
    db.add(s); db.commit(); db.refresh(s)
    return s

def pause_session(db: Session, session_id: int):
    s = db.query(models.FocusSession).filter(models.FocusSession.id == session_id).first()
    if not s:
        return None
    if s.paused or s.status != "running":
        return s
    now = datetime.utcnow()
    s.paused = True
    s.paused_at = now
    s.remaining_seconds = int((s.end_time - now).total_seconds())
    s.status = "paused"
    db.commit(); db.refresh(s)
    return s

def resume_session(db: Session, session_id: int):
    s = db.query(models.FocusSession).filter(models.FocusSession.id == session_id).first()
    if not s:
        return None
    if not s.paused:
        return s
    now = datetime.utcnow()
    s.end_time = now + timedelta(seconds=s.remaining_seconds or 0)
    s.paused = False
    s.paused_at = None
    s.remaining_seconds = None
    s.status = "running"
    db.commit(); db.refresh(s)
    return s

def list_active_sessions(db: Session, user_id: int):
    now = datetime.utcnow()
    return db.query(models.FocusSession).filter(
        models.FocusSession.user_id == user_id,
        models.FocusSession.status == "running",
        models.FocusSession.end_time > now
    ).all()

def list_sessions_for_user(db: Session, user_id: int):
    return db.query(models.FocusSession)\
        .filter(models.FocusSession.user_id == user_id)\
        .order_by(models.FocusSession.start_time.desc())\
        .all()

def list_all_sessions(db: Session):
    """Every session across every user, newest first — this is what actually
    lets you browse 'who completed what, when' like an admin/analytics view."""
    return db.query(models.FocusSession)\
        .order_by(models.FocusSession.start_time.desc())\
        .all()
# =========================
# BLOCKED APPS
# =========================
def create_blocked_apps_for_session(db: Session, user_id: int, package_names: List[str], duration_minutes: int, app_names=None):
    now = datetime.utcnow()
    end = now + timedelta(minutes=duration_minutes)
    created = []
    for i, pkg in enumerate(package_names):
        app_name = app_names[i] if app_names and len(app_names) > i else None
        b = models.BlockedApp(
            user_id=user_id,
            package_name=pkg,
            app_name=app_name,
            start_time=now,
            end_time=end,
            is_active=True
        )
        db.add(b)
        created.append(b)
    db.commit()
    for c in created: db.refresh(c)
    return created

def list_active_blocked_apps(db: Session, user_id: int):
    now = datetime.utcnow()
    return db.query(models.BlockedApp).filter(
        models.BlockedApp.user_id == user_id,
        models.BlockedApp.is_active == True,
        models.BlockedApp.end_time > now
    ).all()

def deactivate_expired_blocks(db: Session):
    now = datetime.utcnow()
    expired = db.query(models.BlockedApp).filter(
        models.BlockedApp.is_active == True,
        models.BlockedApp.end_time <= now
    ).all()
    for e in expired:
        e.is_active = False
    db.commit()
    return expired

def stop_session(db: Session, session_id: int):
    s = db.query(models.FocusSession).filter(models.FocusSession.id == session_id).first()
    if not s:
        return None
    if s.status in ("stopped", "finished"):
        return s  # already stopped — idempotent, avoids double-counting stats
    now = datetime.utcnow()
    s.end_time = now          # lock in actual elapsed time, not the originally scheduled end
    s.paused = False
    s.paused_at = None
    s.remaining_seconds = None
    s.status = "stopped"
    db.commit()
    db.refresh(s)
    # Now that end_time reflects real elapsed time, record it in stats/streak
    update_after_session_completion(db, s.user_id, s)
    return s

def stop_session(db: Session, session_id: int):
    s = db.query(models.FocusSession).filter(models.FocusSession.id == session_id).first()
    if not s:
        return None
    if s.status in ("stopped", "finished"):
        return s  # already stopped — idempotent, avoids double-counting stats
    now = datetime.utcnow()
    s.end_time = now          # lock in actual elapsed time, not the originally scheduled end
    s.paused = False
    s.paused_at = None
    s.remaining_seconds = None
    s.status = "stopped"
    db.commit()
    db.refresh(s)
    # Now that end_time reflects real elapsed time, record it in stats/streak
    update_after_session_completion(db, s.user_id, s)
    return s
