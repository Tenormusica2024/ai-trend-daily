"""
データベース操作モジュール
SQLiteを使用してトレンドデータを管理
"""
import sqlite3
import os
from datetime import datetime, timedelta
from config import DB_PATH, DATA_RETENTION_DAYS

class TrendDatabase:
    def __init__(self):
        """データベース接続とテーブル初期化"""
        # dataディレクトリ作成
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """テーブル作成"""
        # トレンドデータテーブル
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                pageviews INTEGER NOT NULL,
                collected_at TIMESTAMP NOT NULL,
                rank INTEGER
            )
        ''')
        
        # インデックス作成
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_collected_at 
            ON trends(collected_at)
        ''')
        
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_keyword 
            ON trends(keyword)
        ''')
        
        self.conn.commit()
    
    def insert_trend(self, keyword, pageviews, rank=None):
        """トレンドデータを挿入"""
        collected_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.cursor.execute('''
            INSERT INTO trends (keyword, pageviews, collected_at, rank)
            VALUES (?, ?, ?, ?)
        ''', (keyword, pageviews, collected_at, rank))
        
        self.conn.commit()
    
    def get_latest_ranking(self, limit=10):
        """最新のランキングを取得"""
        self.cursor.execute('''
            SELECT keyword, pageviews, collected_at, rank
            FROM trends
            WHERE collected_at = (
                SELECT MAX(collected_at) FROM trends
            )
            ORDER BY rank ASC
            LIMIT ?
        ''', (limit,))
        
        return self.cursor.fetchall()
    
    def get_keyword_history(self, keyword, days=7):
        """特定キーワードの履歴を取得"""
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        self.cursor.execute('''
            SELECT keyword, pageviews, collected_at, rank
            FROM trends
            WHERE keyword = ? AND collected_at >= ?
            ORDER BY collected_at DESC
        ''', (keyword, cutoff_date))
        
        return self.cursor.fetchall()
    
    def cleanup_old_data(self):
        """古いデータを削除"""
        cutoff_date = (datetime.now() - timedelta(days=DATA_RETENTION_DAYS)).strftime('%Y-%m-%d')
        
        self.cursor.execute('''
            DELETE FROM trends
            WHERE collected_at < ?
        ''', (cutoff_date,))
        
        deleted = self.cursor.rowcount
        self.conn.commit()
        
        return deleted
    
    def close(self):
        """データベース接続を閉じる"""
        self.conn.close()
