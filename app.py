import sys

sys.path.insert(0, 'src')

from ResearchFlow.config.logging_config import setup_logging
from ResearchFlow.ui.streamlit_app import main


setup_logging()

if __name__ == "__main__":
    main()
