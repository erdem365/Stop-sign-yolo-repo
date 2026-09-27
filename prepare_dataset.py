"""
Kaynak trafik işareti veri setinden (10 sınıf) yalnızca STOP tabelası (class 0)
etiketi içeren görüntüleri filtreleyerek tek sınıflı bir YOLO veri seti üretir.

Kaynak veri seti:
https://github.com/AsadiAhmad/Traffic-sign-detection-using-yolo (MIT lisans)

Kullanım (repo kök dizininden):
    git clone https://github.com/AsadiAhmad/Traffic-sign-detection-using-yolo.git
    python dataset_prep/prepare_dataset.py \
        --src Traffic-sign-detection-using-yolo/Dataset \
        --out stop_sign_yolo_dataset
"""
import argparse
import os
import shutil


def filter_stop_sign(src_root: str, out_root: str, target_class: int = 0) -> None:
    """STOP sınıfına (varsayılan: 0) ait etiketleri içeren görüntü+etiket
    çiftlerini kopyalar; etiket dosyalarında yalnızca STOP kutuları bırakılır."""
    split_map = {"train": "train", "val": "valid"}

    for split_src, split_dst in split_map.items():
        img_src = os.path.join(src_root, "images", split_src)
        lbl_src = os.path.join(src_root, "labels", split_src)
        img_dst = os.path.join(out_root, split_dst, "images")
        lbl_dst = os.path.join(out_root, split_dst, "labels")
        os.makedirs(img_dst, exist_ok=True)
        os.makedirs(lbl_dst, exist_ok=True)

        copied = 0
        for lbl_file in os.listdir(lbl_src):
            with open(os.path.join(lbl_src, lbl_file)) as f:
                lines = f.readlines()

            stop_lines = [
                line for line in lines
                if line.strip() and int(line.split()[0]) == target_class
            ]
            if not stop_lines:
                continue

            base = lbl_file.replace(".txt", "")
            matches = [f for f in os.listdir(img_src) if f.startswith(base + ".")]
            if not matches:
                continue
            img_file = matches[0]

            shutil.copy(os.path.join(img_src, img_file), os.path.join(img_dst, img_file))
            with open(os.path.join(lbl_dst, lbl_file), "w") as out:
                out.writelines(stop_lines)  # class id zaten 0 (tek sınıf)
            copied += 1

        print(f"{split_dst}: {copied} görüntü kopyalandı")

    yaml_content = (
        "train: train/images\n"
        "val: valid/images\n\n"
        "nc: 1\n"
        "names: ['stop_sign']\n"
    )
    with open(os.path.join(out_root, "data.yaml"), "w") as f:
        f.write(yaml_content)
    print(f"data.yaml yazıldı -> {out_root}/data.yaml")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, help="Kaynak Dataset/ klasörü")
    parser.add_argument("--out", required=True, help="Çıktı veri seti klasörü")
    parser.add_argument("--target-class", type=int, default=0, help="STOP sınıfının id'si")
    args = parser.parse_args()

    filter_stop_sign(args.src, args.out, args.target_class)
