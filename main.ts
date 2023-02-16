import axios from "axios";
import {parseEDNString} from "edn-data";

const sleep = async (ms: number) => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

const main = async () => {
  const res = await axios.get("https://firestore.googleapis.com/v1/projects/leverheads-278521/databases/(default)/documents/symphony/rS2JIupnK25fu6W04W4a");
  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
  // console.log(res.data);

  const k: any = parseEDNString(res.data.fields.latest_version_edn.stringValue);
  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
  console.log(k.map[6][1][0].map);
};

void (async () => await main())();