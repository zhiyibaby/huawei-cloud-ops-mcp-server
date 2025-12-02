"""
日志模块 - 提供统一的日志配置和管理
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

from huawei_cloud_ops_mcp_server.config import _project_root


def setup_logger(
    name: str = 'huawei_cloud_ops_mcp_server',
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
    console_output: bool = True,
    file_output: bool = True,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    设置并返回配置好的日志记录器

    Args:
        name: 日志记录器名称
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                  如果为 None,则从环境变量 LOG_LEVEL 读取,默认为 INFO
        log_file: 日志文件路径
                  如果为 None,则从环境变量 LOG_FILE 读取,默认为 logs/app.log
        console_output: 是否输出到控制台,默认 True
        file_output: 是否输出到文件,默认 True
        max_bytes: 日志文件最大大小(字节),默认 10MB
        backup_count: 保留的备份文件数量,默认 5

    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 获取日志级别
    if log_level is None:
        from huawei_cloud_ops_mcp_server.config import LogConfig
        log_level = LogConfig.get_level()

    # 获取日志文件路径
    if log_file is None:
        from huawei_cloud_ops_mcp_server.config import LogConfig
        log_file = LogConfig.get_file()

    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 日志格式
    detailed_format = (
        '%(asctime)s - %(name)s - %(levelname)s - '
        '%(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
    )
    simple_format = '%(asctime)s - %(levelname)s - %(message)s'

    formatter = logging.Formatter(
        detailed_format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter(
        simple_format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 控制台处理器
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level, logging.INFO))
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)

    # 文件处理器
    if file_output:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, log_level, logging.INFO))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# 创建默认的日志记录器实例
logger = setup_logger()
