import argparse
import pathlib
import json
import subprocess
import shutil

import numpy as np
import pandas as pd
import jinja2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=pathlib.Path)
    parser.add_argument("out", type=pathlib.Path)
    parser.add_argument("--filter", nargs="*")
    options = parser.parse_args()

    base: pathlib.Path = options.base
    out: pathlib.Path = options.out

    drawings = pd.read_excel(base / "Metadaten.ods", sheet_name="Zeichnungen")
    paper = pd.read_excel(base / "Metadaten.ods", sheet_name="Papiere")

    df = pd.merge(drawings, paper, how="left")
    df.sort_values("Dateiname", ascending=False, inplace=True)
    df.index = df["Dateiname"]
    del df["Dateiname"]

    images_with_meta = set(df.index)
    images_in_dir = {path.stem for path in base.glob("*.jpg")}
    images_without_meta = images_in_dir - images_with_meta
    if images_without_meta:
        print("Images without meta data:")
        for image in sorted(images_without_meta):
            print(image)

    df["Jahr"] = [int(i[:4]) for i in df.index]

    for f in options.filter:
        key, value = f.split("=")
        df = df.loc[df[key] == value].copy()
        del df[key]

    unique = {
        col: sorted(simplify(v) for v in df[col].unique() if not pd.isna(v))
        for col in sorted(df.columns)
    }

    records = df.to_dict("index")

    env = jinja2.Environment(
        loader=jinja2.PackageLoader("zeichnungsgallerie"),
        autoescape=jinja2.select_autoescape(),
    )

    template = env.get_template("index.html.j2")
    rendered = template.render(
        unique=unique, records=records, variables=list(unique.keys())
    )

    out.mkdir(parents=True, exist_ok=True)
    with open(out / "index.html", "w") as f:
        f.write(rendered)

    with open(out / "metadata.json", "w") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    for stem in df.index:
        picture = base / f"{stem}.jpg"
        thumbnail = out / "small" / picture.name
        preview = out / "big" / picture.name

        thumbnail.parent.mkdir(exist_ok=True)
        preview.parent.mkdir(exist_ok=True)

        if not thumbnail.exists():
            subprocess.run(
                [
                    "magick",
                    str(picture),
                    "-resize",
                    "300x300>",
                    str(thumbnail),
                ],
                check=True,
            )
        if not preview.exists():
            subprocess.run(
                [
                    "magick",
                    str(picture),
                    "-resize",
                    "2000x2000>",
                    str(preview),
                ],
                check=True,
            )

    shutil.copytree(pathlib.Path(__file__).parent / "static", out / "static")


def simplify(v):
    if isinstance(v, np.int64):
        return int(v)
    else:
        return v


if __name__ == "__main__":
    main()
