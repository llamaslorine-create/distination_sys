import requests
import logging
from config import OLLAMA_API_URL, OLLAMA_MODEL

# 配置日志
logger = logging.getLogger(__name__)


def ask_ai(question):
    """调用Ollama API进行问答

    Args:
        question: 问题字符串

    Returns:
        str: AI回答的内容
    """
    try:
        # 验证问题是否为空
        if not question or not question.strip():
            return '请输入有效的问题'

        # 调用Ollama API
        response = requests.post(
            f"{OLLAMA_API_URL}/generate",
            json={
                "model": OLLAMA_MODEL,  # 使用配置的模型
                "prompt": question,  # 问题
                "stream": False  # 不使用流式响应
            },
            timeout=30  # 设置超时时间
        )

        # 检查响应状态
        response.raise_for_status()

        # 解析响应数据
        data = response.json()
        return data.get('response', 'AI暂时无法回答')

    except requests.exceptions.ConnectionError:
        logger.error("Ollama服务连接失败，请检查服务是否启动")
        return '网络连接失败，请检查Ollama服务是否正常运行'

    except requests.exceptions.Timeout:
        logger.error("Ollama请求超时")
        return '请求超时，请稍后重试'

    except requests.exceptions.HTTPError as e:
        logger.error(f"Ollama请求HTTP错误: {e}")
        return f'请求失败，错误码: {response.status_code}'

    except ValueError:
        logger.error("Ollama响应解析失败")
        return '响应解析失败，请稍后重试'

    except Exception as e:
        logger.error(f"AI调用失败: {e}")
        return 'AI暂时无法回答'