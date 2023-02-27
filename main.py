from datetime import date
from edn_format import Keyword as K, dumps, loads
from requests import get
from uuid import uuid4

# Want:
# '{
#   :id "huITjpduEDhgyxVQ7sYb",
#   :step :root,
#   :name "Merged Symph",
#   :description "",
#   :rebalance :none,
#   :rebalance-corridor-width 0.1,
#   :children [{
#     :id "b2c43189-f09a-470d-812d-499163ca2feb",
#     :step :wt-cash-specified,
#     :children [{
#       :name "SPDR S&P 500 ETF Trust",
#       :ticker "SPY",
#       :has_marketcap false,
#       :weight {:num "50", :den 100},
#       :id "62e81815-a15c-401f-bb07-177fa3ae4380",
#       :exchange "ARCX",
#       :price 396.38,
#       :step :asset,
#       :dollar_volume 42886101424.94
#     } {
#       :name "Invesco QQQ Trust",
#       :ticker "QQQ",
#       :has_marketcap false,
#       :weight {:num "50", :den 100},
#       :id "a70d028b-80ba-49ac-8578-89ab99ca5d37",
#       :exchange "XNAS",
#       :price 291.85,
#       :step :asset,
#       :dollar_volume 21693781942.300003
#     }
#   ]}],
#   :suppress-incomplete-warnings? false
# }'
# Actual
# {
#   :id "huITjpduEDhgyxVQ7sYb"
#   :step :root
#   :name "Merged Symph, updated 2023-02-26"
#   :description "Merge of multiple symphonies by weight, last updated 2023-02-26\nhuITjpduEDhgyxVQ7sYb: 50%\nhuITjpduEDhgyxVQ7sYb: 50%\n\nCreated using composer-utils by geoff"
#   :rebalance :daily
#   :children [{
#     :id "17f491af-4ea4-46cc-8bd2-5566e50d7458"
#     :step :wt-cash-specified
#     :children [{
#       :weight {:num 50 :den 100}
#       :children [{
#         :id "b2c43189-f09a-470d-812d-499163ca2feb"
#         :step :wt-cash-equal
#         :children [{
#           :name "SPDR S&P 500 ETF Trust"
#           :ticker "SPY"
#           :has_marketcap false
#           :id "79b256d0-20b4-48ca-912a-ea28fb148524"
#           :exchange "ARCX"
#           :price 396.38
#           :step :asset
#           :dollar_volume 42886101424.94
#         }]
#       }]
#     } {
#       :weight {:num 50 :den 100}
#       :children [{
#         :id "b2c43189-f09a-470d-812d-499163ca2feb"
#         :step :wt-cash-equal
#         :children [{
#           :name "SPDR S&P 500 ETF Trust"
#           :ticker "SPY"
#           :has_marketcap false
#           :id "79b256d0-20b4-48ca-912a-ea28fb148524"
#           :exchange "ARCX"
#           :price 396.38
#           :step :asset
#           :dollar_volume 42886101424.94
#         }]
#       }]
#     }]
#   }]
# }

def get_symph_edn(symphony_id) -> str:
    url = "https://firestore.googleapis.com/v1/projects/leverheads-278521/databases/(default)/documents/symphony/" +symphony_id
    res = get(url)
    edn_str = res.json()["fields"]["latest_version_edn"]["stringValue"]
    return loads(edn_str)

def get_symph_child(symph_id: str, weight: int):
    return {
        K("weight"): {
            K("num"): weight,
            K("den"): 100
        },
        K("children"): get_symph_edn(symph_id).get(K("children"))
    }

def get_merged_symph_children(symph_weights: list[tuple[str, int]]):
    return [get_symph_child(symph_id, weight) for (symph_id, weight) in symph_weights]

def get_descr(date_str: str, symph_weights: list[tuple[str, int]]) -> str:
    descr_str = "Merge of multiple symphonies by weight, last updated " + date_str + "\n"
    for symph_id, weight in symph_weights:
        descr_str += symph_id + ": " + weight.__str__() + "%\n"
    descr_str += "\nCreated using composer-utils by geoff"
    return descr_str

mergable_edn = get_symph_edn("huITjpduEDhgyxVQ7sYb")
symph_weights = [("huITjpduEDhgyxVQ7sYb", 50), ("huITjpduEDhgyxVQ7sYb", 50)]

date_str = date.today().strftime("%Y-%m-%d")
merged_obj = {
    K("id"): mergable_edn.get(K("id")),
    K("step"): K("root"),
    K("name"): "Merged Symph, updated " + date_str,
    K("description"): get_descr(date_str, symph_weights),
    K("rebalance"): K("daily"),
    K("children"): [{
        K("id"): str(uuid4()),
        K("step"): K("wt-cash-specified"),
        K("children"): get_merged_symph_children(symph_weights)
    }]
}

print(dumps(merged_obj))