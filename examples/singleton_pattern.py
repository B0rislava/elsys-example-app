"""
Singleton Pattern Implementation in Python

This example demonstrates a Singleton pattern implementation for FileStorageManager,
which manages centralized file storage.
"""

import threading
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class FileStorageManager:
    """
    Singleton class for file management.
    Ensures only one instance exists in the application.
    """

    _instance: Optional['FileStorageManager'] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls):
        """
        Thread-safe implementation of Singleton pattern.
        Uses double-checked locking for better performance.
        """
        if cls._instance is None:
            with cls._lock:
                # Double-check inside the lock for thread safety
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Initialize the singleton instance.
        This method is called every time, but initializes only once.
        """
        if self._initialized:
            return

        self.storage_path = Path("storage")
        self.storage_path.mkdir(exist_ok=True)

        self.files_metadata: Dict[str, Dict[str, Any]] = {}
        self.total_uploads = 0
        self.created_at = datetime.now()

        self._initialized = True
        print(f"FileStorageManager initialized at {self.created_at}")

    def upload_file(self, filename: str, content: bytes) -> Dict[str, Any]:
        """
        Upload a file to the storage directory.

        Args:
            filename: Name of the file
            content: File content as bytes

        Returns:
            Metadata of the uploaded file
        """
        file_path = self.storage_path / filename

        # Write the file
        with open(file_path, 'wb') as f:
            f.write(content)

        # Store metadata
        metadata = {
            'filename': filename,
            'size': len(content),
            'uploaded_at': datetime.now().isoformat(),
            'path': str(file_path)
        }

        self.files_metadata[filename] = metadata
        self.total_uploads += 1

        return metadata

    def get_file(self, filename: str) -> Optional[bytes]:
        """
        Retrieve a file from storage.

        Args:
            filename: Name of the file

        Returns:
            File content or None if it doesn't exist
        """
        file_path = self.storage_path / filename

        if not file_path.exists():
            return None

        with open(file_path, 'rb') as f:
            return f.read()

    def list_files(self) -> Dict[str, Any]:
        """
        Return a list of all files and statistics.

        Returns:
            Information about stored files
        """
        return {
            'files': list(self.files_metadata.keys()),
            'total_files': len(self.files_metadata),
            'total_uploads': self.total_uploads,
            'manager_uptime': str(datetime.now() - self.created_at)
        }

    def get_statistics(self) -> Dict[str, Any]:
        """
        Return statistics about the storage manager.

        Returns:
            Statistical data
        """
        total_size = sum(
            metadata['size']
            for metadata in self.files_metadata.values()
        )

        return {
            'total_files': len(self.files_metadata),
            'total_uploads': self.total_uploads,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'created_at': self.created_at.isoformat(),
            'uptime_seconds': (datetime.now() - self.created_at).total_seconds()
        }

    def delete_file(self, filename: str) -> bool:
        """
        Delete a file from storage.

        Args:
            filename: Name of the file to delete

        Returns:
            True if the file was deleted successfully, False otherwise
        """
        file_path = self.storage_path / filename

        if not file_path.exists():
            return False

        file_path.unlink()

        if filename in self.files_metadata:
            del self.files_metadata[filename]

        return True


# Demonstration of Singleton pattern
def demo_singleton():
    """
    Demonstrates how the Singleton pattern works.
    """
    print("=== Singleton Pattern Demo ===\n")

    # Create first instance
    manager1 = FileStorageManager()
    print(f"Manager 1 ID: {id(manager1)}")

    # Attempt to create second instance
    manager2 = FileStorageManager()
    print(f"Manager 2 ID: {id(manager2)}")

    # Check if they are the same instance
    print(f"\nManager 1 and Manager 2 are the same: {manager1 is manager2}")

    # Upload file via first instance
    print("\n--- Uploading file via manager1 ---")
    manager1.upload_file("test.txt", b"Hello from Singleton!")

    # Access the same file via second instance
    print("\n--- Accessing file via manager2 ---")
    content = manager2.get_file("test.txt")
    print(f"File content: {content.decode('utf-8')}")

    # Show statistics
    print("\n--- Statistics ---")
    stats = manager1.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")

    # List files
    print("\n--- File List ---")
    files_info = manager2.list_files()
    print(files_info)


# Thread-safety demonstration
def demo_thread_safety():
    """
    Demonstrates thread-safety of the Singleton implementation.
    """
    import concurrent.futures

    print("\n\n=== Thread Safety Demo ===\n")

    instances = []

    def create_instance(thread_id):
        """Create an instance in a separate thread"""
        manager = FileStorageManager()
        instances.append(id(manager))
        return id(manager)

    # Create instances in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_instance, i) for i in range(10)]
        results = [future.result() for future in futures]

    # Check if all instances have the same ID
    print(f"All instances have the same ID: {len(set(results)) == 1}")
    print(f"Unique instance IDs: {set(results)}")


if __name__ == "__main__":
    # Run demonstrations
    demo_singleton()
    demo_thread_safety()