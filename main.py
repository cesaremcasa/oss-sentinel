import sys
from pathlib import Path

# Adiciona o 'src' ao path para que possamos importar nossos módulos
sys.path.append(str(Path(__file__).resolve().parent))

from src.ingestion import main as run_ingestion

if __name__ == "__main__":
    print("Iniciando OSS Sentinel Pipeline...")
    try:
        run_ingestion()
    except Exception as e:
        print(f"Falha na execução do pipeline: {e}")
