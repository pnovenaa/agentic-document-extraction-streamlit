from pathlib import Path

from PIL import Image, ImageDraw


class Visualizer:

    @staticmethod
    def draw_chunk_box(document_path: Path, chunk):

        ext = document_path.suffix.lower()
        print(document_path)
        print(ext)

        if ext == ".pdf":

            try:
                from pdf2image import convert_from_path
            except ImportError:
                raise ImportError(
                    "pdf2image is required for PDF preview.\n"
                    "Install it with:\n\n"
                    "pip install pdf2image\n"
                    "brew install poppler"
                )

            image = convert_from_path(
                document_path,
                first_page=chunk.grounding.page + 1,
                last_page=chunk.grounding.page + 1,
            )[0]

            image = image.convert("RGB")

        else:

            image = Image.open(document_path).convert("RGB")

        draw = ImageDraw.Draw(image)

        w, h = image.size

        box = chunk.grounding.box

        draw.rectangle(
            [
                box.left * w,
                box.top * h,
                box.right * w,
                box.bottom * h,
            ],
            outline="red",
            width=4,
        )

        return image