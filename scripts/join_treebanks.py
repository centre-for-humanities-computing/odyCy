from typing import Literal, List, Iterable

Purpose = Literal["dev", "test", "train"]

PURPOSES: List[Purpose] = ["dev", "test", "train"]


def get_conllu_paths(purpose: Purpose) -> List[str]:
    """Returns all conllu files for the given purpose."""
    return [
        f"assets/treebanks/proiel/{purpose}.conllu",
        f"assets/treebanks/perseus/{purpose}.conllu",
    ]


def stream_files(paths: Iterable[str]) -> Iterable[str]:
    """Streams through given conllu files."""
    for path in paths:
        with open(path) as in_file:
            yield in_file.read()


def main() -> None:
    print("Joining treebanks:")
    for purpose in PURPOSES:
        print(f" - {purpose}")
        paths = get_conllu_paths(purpose=purpose)
        conllu_contents = stream_files(paths)
        joint_conllu = "".join(conllu_contents)
        out_path = f"assets/treebanks/joint/{purpose}.conllu"
        with open(out_path, "w") as out_file:
            out_file.write(joint_conllu)
    print("DONE")


if __name__ == "__main__":
    main()
