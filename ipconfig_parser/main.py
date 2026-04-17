import json
from pathlib import Path


FIELDS = {
    "description": "Description",
    "physical_address": "Physical Address",
    "dhcp_enabled": "DHCP Enabled",
    "ipv4_address": "IPv4 Address",
    "subnet_mask": "Subnet Mask",
    "default_gateway": "Default Gateway",
    "dns_servers": "DNS Servers"
}


def main():
    input_files = ["parser_input_a.txt", "parser_input_b.txt"]
    output = []

    for filename in input_files:
        file = Path(filename)
        if not file.exists():
            continue

        text = file.read_text(encoding="utf-8", errors="ignore")
        adapters = parse_ipconfig_text(text)

        output.append({
            "file_name": filename,
            "adapters": adapters
        })

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
