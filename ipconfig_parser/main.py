from pathlib import Path
import re
import json


def parse_ipconfig_output(raw_text: str) -> list[dict]:
    FIELD_MAP = {
        "description": "description",
        "physical address": "physical_address",
        "dhcp enabled": "dhcp_enabled",
        "ipv4 address": "ipv4_address",
        "autoconfiguration ipv4 address": "ipv4_address",
        "subnet mask": "subnet_mask",
        "default gateway": "default_gateway",
        "dns servers": "dns_servers",
    }

    adapters = []
    current_adapter = None
    last_parsed_field = None

    for line in raw_text.splitlines():
        if (
            not line.startswith((" ", "\t"))
            and "adapter" in line.lower()
            and line.strip().endswith(":")
        ):
            if current_adapter is not None:
                adapters.append(current_adapter)

            current_adapter = {
                "adapter_name": line.strip().rstrip(":"),
                "description": "",
                "physical_address": "",
                "dhcp_enabled": "",
                "ipv4_address": "",
                "subnet_mask": "",
                "default_gateway": "",
                "dns_servers": [],
            }
            continue

        if current_adapter is not None and ":" in line:
            key, value = line.split(":", 1)

            normalized_key = key.replace(".", "").strip().lower()
            normalized_key = " ".join(normalized_key.split())

            cleaned_value = value.strip()
            cleaned_value = re.sub(r"\((Preferred|Deferred|Duplicate|Deprecated|Tentative)\)", "", value, flags=re.IGNORECASE).strip()

            indent_level = len(line) - len(line.lstrip())

            if normalized_key in FIELD_MAP:
                field_name = FIELD_MAP[normalized_key]

                if field_name == "dns_servers":
                    if cleaned_value:
                        current_adapter["dns_servers"].append(cleaned_value)
                    last_parsed_field = field_name
                else:
                    current_adapter[field_name] = cleaned_value
                    last_parsed_field = field_name

            elif last_parsed_field == "dns_servers" and indent_level > 20:
                extra_dns = line.strip()
                if extra_dns:
                    extra_dns = re.sub(r"\(.*?\)", "", extra_dns).strip()
                    current_adapter["dns_servers"].append(extra_dns)

            else:
                last_parsed_field = None

    if current_adapter is not None:
        adapters.append(current_adapter)

    return adapters


def process_ipconfig_files():
    parsed_results = []

    for file_path in sorted(Path(".").glob("*.txt")):
        raw_text = file_path.read_text(encoding="utf-16")
        parsed_results.append({
            "file_name": file_path.name,
            "adapters": parse_ipconfig_output(raw_text),
        })

    json_output = json.dumps(parsed_results, indent=2, ensure_ascii=False)
    print(json_output)
    Path("output.json").write_text(json_output, encoding="utf-8")


if __name__ == "__main__":
    process_ipconfig_files()
