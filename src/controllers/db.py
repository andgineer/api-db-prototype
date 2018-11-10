"""
Inject here database dependency
"""
from sqlalchemy.orm import Session
from typing import Any


session: Session = None
models: Any = None
