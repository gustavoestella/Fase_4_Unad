"""Bitácora de eventos y errores, sin persistencia de datos de negocio."""
import logging
from pathlib import Path

logger = logging.getLogger('software_fj')
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler(Path(__file__).with_name('sistema.log'), encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    logger.addHandler(handler)
