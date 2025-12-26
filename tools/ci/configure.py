from pathlib import Path

import shutil

assets_dir = Path(__file__).parent.parent.parent.resolve() / "assets"


def configure_ocr_model():
    assets_ocr_dir = assets_dir / "MaaCommonAssets" / "OCR"
    if not assets_ocr_dir.exists():
        print(f"File Not Found: {assets_ocr_dir}")
        exit(1)

    resource_root = assets_dir / "resource"
    if not resource_root.exists() or not resource_root.is_dir():
        print(f"Resource directory not found: {resource_root}")
        exit(1)

    src_model_dir = assets_ocr_dir / "ppocr_v5" / "zh_cn"
    if not src_model_dir.exists():
        print(f"Source OCR model not found: {src_model_dir}")
        exit(1)

    # Iterate through all version directories under assets/resource and install OCR model if missing
    for version_dir in resource_root.iterdir():
        if not version_dir.is_dir():
            continue

        ocr_dir = version_dir / "model" / "ocr"
        if not ocr_dir.exists():
            print(f"Importing default OCR model into: {ocr_dir}")
            ocr_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(
                src_model_dir,
                ocr_dir,
                dirs_exist_ok=True,
            )
        else:
            print(f"Found existing OCR directory for '{version_dir.name}', skipping.")


if __name__ == "__main__":
    configure_ocr_model()

    print("OCR model configured.")
