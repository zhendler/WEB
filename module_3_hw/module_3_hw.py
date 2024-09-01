import os
import shutil
import concurrent.futures

def copy_and_sort(source_dir, target_dir="dist"):
    """
    Копіює та сортує файли за розширенням у вказаній директорії.
    в командному рядку вказуємо : "python module_3_hw.py pictures"

    Args:
        source_dir: Назва  вихідної папки (має бути в поточній директорії).
        target_dir: Шлях до нової папки (за замовчуванням - "dist").
    """

    full_source_dir = os.path.join(os.getcwd(), source_dir)

    if not os.path.exists(full_source_dir):
        print(f"Директорія {full_source_dir} не існує.")
        return

    os.makedirs(target_dir, exist_ok=True)

    def process_directory(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                source_file = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                target_subdir = os.path.join(target_dir, ext[1:])
                os.makedirs(target_subdir, exist_ok=True)
                target_file = os.path.join(target_subdir, file)
                shutil.copy2(source_file, target_file)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(process_directory, full_source_dir)

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print("Не вказано назву директорії для сортування.")
		sys.exit(1)

	source_dir = sys.argv[1]
	copy_and_sort(source_dir)