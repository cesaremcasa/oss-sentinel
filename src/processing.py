import pandas as pd
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProcessingEngine:
    def __init__(self, raw_dir="data/raw", processed_dir="data/processed"):
        base_dir = Path(__file__).resolve().parent.parent
        self.raw_dir = base_dir / raw_dir
        self.processed_dir = base_dir / processed_dir
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def load_raw_data(self, filepath: Path) -> List[Dict[str, Any]]:
        """Carrega o JSON bruto. Aceita lista ou dict com 'items'."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'items' in data:
                return data['items']
            else:
                logger.error(f"Formato JSON inválido no arquivo {filepath.name}")
                return []
        except Exception as e:
            logger.error(f"Erro ao ler {filepath.name}: {e}")
            return []

    def normalize_github_data(self, raw_items: List[Dict]) -> pd.DataFrame:
        """Normaliza dados de Issues para o Schema padrão."""
        if not raw_items:
            return pd.DataFrame()

        processed_data = []

        for item in raw_items:
            # Mapeamento de campos (API -> Schema)
            user_login = item.get('user', {}).get('login', 'Unknown')
            labels_list = item.get('labels', [])
            labels_str = ", ".join([l.get('name', '') for l in labels_list])

            record = {
                "id": item.get("id"),
                "number": item.get("number"),
                "title": item.get("title"),
                "state": item.get("state"),
                "created_at": item.get("created_at"),
                "closed_at": item.get("closed_at"),
                "author": user_login,
                "body": item.get("body") or "",
                "comments_count": item.get("comments"),
                "labels": labels_str,
                "url": item.get("html_url")
            }
            processed_data.append(record)

        df = pd.DataFrame(processed_data)
        
        # Ordenação das colunas
        cols = [
            "id", "number", "title", "state", "body", 
            "author", "comments_count", "labels", "url", 
            "created_at", "closed_at"
        ]
        df = df[[c for c in cols if c in df.columns]]
        
        return df

    def save_processed_data(self, df: pd.DataFrame, output_filename_base: str):
        """
        Salva o CSV e JSON.
        output_filename_base: ex: 'processed_apache_superset'
        """
        if df.empty:
            logger.warning(f"DataFrame vazio para {output_filename_base}. Pulando salvamento.")
            return

        # Adiciona timestamp ao arquivo de saída para versionamento
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        
        csv_path = self.processed_dir / f"{output_filename_base}_{timestamp}.csv"
        df.to_csv(csv_path, index=False)
        logger.info(f"CSV salvo: {csv_path}")

        json_path = self.processed_dir / f"{output_filename_base}_{timestamp}.json"
        df.to_json(json_path, orient='records', indent=4)

    def run_batch(self):
        """
        Varre a pasta data/raw e processa todos os arquivos .json encontrados.
        """
        raw_files = list(self.raw_dir.glob("*.json"))
        
        if not raw_files:
            logger.warning("Nenhum arquivo .json encontrado em data/raw.")
            return

        # Ordena para garantir processamento consistente (opcional)
        raw_files.sort()

        logger.info(f"Iniciando processamento em lote. {len(raw_files)} arquivos encontrados.")

        for raw_file in raw_files:
            logger.info(f"--- Processando: {raw_file.name} ---")
            
            # 1. Extrair o nome base do arquivo para criar o nome de saída
            # Input: ingest_apache_superset_20231223_120000.json
            # Lógica: Remove timestamp do final (últimos 2 separadores _) e prefixo 'ingest_'
            stem = raw_file.stem  # ingest_apache_superset_20231223_120000
            parts = stem.rsplit('_', 2) # ['ingest_apache_superset', '20231223', '120000']
            
            if len(parts) >= 3:
                core_name = parts[0].replace("ingest_", "")
                output_name = f"processed_{core_name}"
            else:
                # Fallback se o nome estiver estranho
                output_name = f"processed_{stem}"

            # 2. Carregar
            raw_data = self.load_raw_data(raw_file)
            
            # 3. Normalizar
            df_clean = self.normalize_github_data(raw_data)
            
            # 4. Salvar
            self.save_processed_data(df_clean, output_name)
            
            logger.info(f"Concluído: {raw_file.name} -> {output_name}")

def main():
    engine = ProcessingEngine()
    engine.run_batch()

if __name__ == "__main__":
    main()
