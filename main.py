from datetime import date
from edn_format import Keyword as K, dumps, loads
from requests import get
from uuid import uuid4
import sys

def get_symph_edn(symphony_id) -> str:
    url = "https://firestore.googleapis.com/v1/projects/leverheads-278521/databases/(default)/documents/symphony/" + symphony_id
    res = get(url)
    edn_str = res.json()["fields"]["latest_version_edn"]["stringValue"]
    return loads(edn_str)

def get_symph_child(weight: int, edn):
    return {
        K("id"): edn.get(K("id")),
        K("name"): edn.get(K("name")),
        K("step"): K("group"),
        K("weight"): {
            K("num"): weight,
            K("den"): 100
        },
        K("children"): edn.get(K("children"))
    }

def get_symph_children(symph_edns: list[tuple[str, int, dict]]):
    return [get_symph_child(weight, edn) for (_, weight, edn) in symph_edns]

def get_descr(date_str: str, symph_edns: list[tuple[str, int, dict]]) -> str:
    weights_str = ", ".join(["({}: {}%)".format(edn.get(K("name"))[0:16], weight) for (_, weight, edn) in symph_edns])
    return "Merge of multiple symphonies by weight, last updated {}. \nWeights = {}. \nCreated using composer-utils by geoff.".format(date_str, weights_str)

def get_merged_symph_edn(mergable_symph_id: str, symph_weights: list[tuple[str, int]]):
    date_str = date.today().strftime("%Y-%m-%d")
    symph_edns = [(id, weight, get_symph_edn(id)) for (id, weight) in symph_weights]
    return {
        K("id"): mergable_symph_id,
        K("step"): K("root"),
        K("name"): "Merged Symph, updated " + date_str,
        K("description"): get_descr(date_str, symph_edns),
        K("rebalance"): K("daily"),
        K("children"): [{
            K("id"): str(uuid4()),
            K("step"): K("wt-cash-specified"),
            K("children"): get_symph_children(symph_edns)
        }]
    }

def get_symph_weights(file: str) -> list[tuple[str, int]]:
    symph_weights = []
    with open(file, "r") as reader:
        for line in reader:
            parts = line.split(",")
            symph_weights.append((parts[0], int(parts[1])))
    return symph_weights

def main():
    if len(sys.argv) != 3:
        print("Incorrect number of arguments: needs symph id and csv")
        exit(1)

    mergable_symph_id = sys.argv[1]
    symph_weights = get_symph_weights(sys.argv[2])
    total_weight = sum([weight for (_, weight) in symph_weights])
    if total_weight != 100:
        print("Symphony weights must equal 100")
        exit(1)

    merged_symph_edn = get_merged_symph_edn(mergable_symph_id, symph_weights)
    print(dumps(merged_symph_edn), end="")

main()