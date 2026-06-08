from pathlib import Path

from rembg import new_session

from bgremover.constants import ALLOWED_EXTENSIONS
from bgremover.rembg_wrapper import Models, remove_bg


def process_image(
    input_path: Path,
    output_dir: Path,
    model: Models = "birefnet-portrait",
    session: any = None,
) -> None | Path:
    output_dir.mkdir(exist_ok=True, parents=True)

    if input_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        print(f"🚫 File extension not allowed: {input_path.suffix} ({input_path.name})")
        return None

    try:
        print(f"🔄 Removing background: {input_path.name}")
        output_image = remove_bg(input_path, output_dir, model, session=session)
    except (ValueError, TypeError, KeyError, Exception) as e:
        print(f"🔴 Error with {input_path.name}: {e}")
    else:
        print(f"✅ Success: {output_image.name}")
        return output_image


def process_images(
    input_dir: Path, output_dir: Path, model: Models = "birefnet-portrait"
) -> None:
    if not input_dir.is_dir():
        print(f"🔴 Not a directory: {input_dir}")
        return

    files = [
        f for f in input_dir.rglob("*") 
        if f.is_file() and f.suffix.lower() in ALLOWED_EXTENSIONS
    ]
    
    if not files:
        print(f"⚠️ No supported images found in: {input_dir}")
        return

    print(f"🚀 Starting batch process for {len(files)} images using model: {model}")
    
    # Cria a sessão uma única vez para todas as imagens
    session = new_session(model)
    
    for img_path in files:
        process_image(img_path, output_dir, model, session=session)
    
    print("🏁 Batch processing complete!")


COMMANDS = {
    "process_image": process_image,
    "process_images": process_images,
}
