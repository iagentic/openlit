from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from . import models, schemas
import logging

logger = logging.getLogger(__name__)

def get_time_filter(time_limit: schemas.TimeLimit):
    now = datetime.utcnow()
    if time_limit == schemas.TimeLimit.LAST_HOUR:
        return now - timedelta(hours=1)
    elif time_limit == schemas.TimeLimit.LAST_DAY:
        return now - timedelta(days=1)
    elif time_limit == schemas.TimeLimit.LAST_WEEK:
        return now - timedelta(weeks=1)
    elif time_limit == schemas.TimeLimit.LAST_MONTH:
        return now - timedelta(days=30)
    else:  # ALL_TIME
        return datetime.min

def get_total_requests(db: Session, user_id: str, time_limit: schemas.TimeLimit):
    time_filter = get_time_filter(time_limit)
    return db.query(func.count(models.Metrics.id)).filter(
        models.Metrics.user_id == user_id,
        models.Metrics.type == "request",
        models.Metrics.timestamp >= time_filter
    ).scalar()

def get_requests_per_time(db: Session, user_id: str, time_limit: schemas.TimeLimit):
    time_filter = get_time_filter(time_limit)
    return db.query(
        func.date_trunc('hour', models.Metrics.timestamp).label('hour'),
        func.count(models.Metrics.id).label('count')
    ).filter(
        models.Metrics.user_id == user_id,
        models.Metrics.type == "request",
        models.Metrics.timestamp >= time_filter
    ).group_by('hour').order_by('hour').all()

def get_average_request_duration(db: Session, user_id: str, time_limit: schemas.TimeLimit):
    time_filter = get_time_filter(time_limit)
    result = db.query(func.avg(models.Metrics.value)).filter(
        models.Metrics.user_id == user_id,
        models.Metrics.type == "request",
        models.Metrics.operation_type == "duration",
        models.Metrics.timestamp >= time_filter
    ).scalar()
    return result or 0

def get_average_gpu_utilization(db: Session, user_id: str, time_limit: schemas.TimeLimit):
    time_filter = get_time_filter(time_limit)
    result = db.query(func.avg(models.GPUMetrics.utilization)).filter(
        models.GPUMetrics.user_id == user_id,
        models.GPUMetrics.timestamp >= time_filter
    ).scalar()
    return result or 0

def get_gpu_utilization_per_time(db: Session, user_id: str, time_limit: schemas.TimeLimit):
    time_filter = get_time_filter(time_limit)
    return db.query(
        func.date_trunc('hour', models.GPUMetrics.timestamp).label('hour'),
        func.avg(models.GPUMetrics.utilization).label('utilization')
    ).filter(
        models.GPUMetrics.user_id == user_id,
        models.GPUMetrics.timestamp >= time_filter
    ).group_by('hour').order_by('hour').all()

def get_average_gpu_temperature(db: Session, user_id: str, time_limit: schemas.TimeLimit):
    time_filter = get_time_filter(time_limit)
    result = db.query(func.avg(models.GPUMetrics.temperature)).filter(
        models.GPUMetrics.user_id == user_id,
        models.GPUMetrics.timestamp >= time_filter
    ).scalar()
    return result or 0

def get_vector_metrics_by_environment(db: Session, user_id: str, time_limit: schemas.TimeLimit):
    time_filter = get_time_filter(time_limit)
    return db.query(
        models.VectorMetrics.environment,
        func.count(models.VectorMetrics.id).label('count')
    ).filter(
        models.VectorMetrics.user_id == user_id,
        models.VectorMetrics.timestamp >= time_filter
    ).group_by(models.VectorMetrics.environment).all()

def get_vector_metrics_by_system(db: Session, user_id: str, time_limit: schemas.TimeLimit):
    time_filter = get_time_filter(time_limit)
    return db.query(
        models.VectorMetrics.system,
        func.count(models.VectorMetrics.id).label('count')
    ).filter(
        models.VectorMetrics.user_id == user_id,
        models.VectorMetrics.timestamp >= time_filter
    ).group_by(models.VectorMetrics.system).all()

def get_vector_metrics_by_application(db: Session, user_id: str, time_limit: schemas.TimeLimit):
    time_filter = get_time_filter(time_limit)
    return db.query(
        models.VectorMetrics.application,
        func.count(models.VectorMetrics.id).label('count')
    ).filter(
        models.VectorMetrics.user_id == user_id,
        models.VectorMetrics.timestamp >= time_filter
    ).group_by(models.VectorMetrics.application).all()

def get_llm_metrics_by_endpoint(db: Session, user_id: str, time_limit: schemas.TimeLimit):
    time_filter = get_time_filter(time_limit)
    return db.query(
        models.LLMMetrics.endpoint,
        func.count(models.LLMMetrics.id).label('count'),
        func.sum(models.LLMMetrics.token_count).label('total_tokens')
    ).filter(
        models.LLMMetrics.user_id == user_id,
        models.LLMMetrics.timestamp >= time_filter
    ).group_by(models.LLMMetrics.endpoint).all()

def get_average_tokens_per_request(db: Session, user_id: str, time_limit: schemas.TimeLimit):
    time_filter = get_time_filter(time_limit)
    result = db.query(func.avg(models.LLMMetrics.token_count)).filter(
        models.LLMMetrics.user_id == user_id,
        models.LLMMetrics.timestamp >= time_filter
    ).scalar()
    return result or 0 