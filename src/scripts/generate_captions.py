import argparse
import os

from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForCausalLM


# A script to generate captions for a directory full of image files for lora training

image_extensions = (".png", ".jpg")


def write_caption_file(dir: str, image_filename: str, caption: str):
    file_name = os.path.splitext(image_filename)[0]
    with open(os.path.join(dir, f"{file_name}.txt"), "w") as file:
        # Write text to the file
        file.write(caption)


def read_image_files(dir: str) -> list[str]:
    return [file for file in os.listdir(dir) if file.lower().endswith(image_extensions)]


def create_captions(dir: str, concept_sentence: str):
    print(f"create captions dir={dir} concept_sentence={concept_sentence}")
    print(f"concept sentence {concept_sentence}")
    # Load internally to not consume resources for training
    if not torch.cuda.is_available():
        print("Cuda is not available for torch")
        raise RuntimeError("Cuda is not available for this torch install.")

    torch_dtype = torch.float16
    model = AutoModelForCausalLM.from_pretrained(
        "multimodalart/Florence-2-large-no-flash-attn",
        torch_dtype=torch_dtype,
        trust_remote_code=True,
    ).to("cuda")
    processor = AutoProcessor.from_pretrained(
        "multimodalart/Florence-2-large-no-flash-attn", trust_remote_code=True
    )

    images_files = read_image_files(dir=dir)

    for i, image_filename in enumerate(images_files):
        image_path = os.path.join(dir, image_filename)
        image = Image.open(image_path).convert("RGB")

        prompt = "<DETAILED_CAPTION>"
        inputs = processor(text=prompt, images=image, return_tensors="pt").to(
            "cuda", torch_dtype
        )
        print(f"inputs {inputs}")

        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3,
        )
        print(f"generated_ids {generated_ids}")

        generated_text = processor.batch_decode(
            generated_ids, skip_special_tokens=False
        )[0]
        print(f"generated_text: {generated_text}")
        parsed_answer = processor.post_process_generation(
            generated_text, task=prompt, image_size=(image.width, image.height)
        )
        print(f"parsed_answer = {parsed_answer}")
        caption_text = parsed_answer["<DETAILED_CAPTION>"].replace(
            "The image shows ", ""
        )
        print(f"caption_text = {caption_text}, concept_sentence={concept_sentence}")
        if concept_sentence:
            caption_text = f"{concept_sentence} {caption_text}"

        write_caption_file(dir=dir, image_filename=image_filename, caption=caption_text)

    model.to("cpu")
    del model
    del processor
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument("image_dir", help="The path to the image directory")
    parser.add_argument("concept", help="The concept sentence, unique or rare word")
    args = parser.parse_args()
    create_captions(dir=args.image_dir, concept_sentence=args.concept)
