import argparse
import pathlib
import json
import subprocess

import pandas as pd
import jinja2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=pathlib.Path)
    parser.add_argument("out", type=pathlib.Path)
    options = parser.parse_args()

    base: pathlib.Path = options.base
    out: pathlib.Path = options.out

    drawings = pd.read_excel(base / "Metadaten.ods", sheet_name="Zeichnungen")
    paper = pd.read_excel(base / "Metadaten.ods", sheet_name="Papiere")

    df = pd.merge(drawings, paper, how="left")
    df.index = df["Dateiname"]
    del df["Dateiname"]

    df["Jahr"] = [int(i[:4]) for i in df.index]

    unique = {
        col: sorted(v for v in df[col].unique() if not pd.isna(v))
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


if __name__ == "__main__":
    main()
