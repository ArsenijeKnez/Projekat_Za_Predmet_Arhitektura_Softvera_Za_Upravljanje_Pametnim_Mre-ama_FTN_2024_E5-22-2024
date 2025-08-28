import xml.etree.ElementTree as ET
import sys
import os


def parse_rdfs(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
        'cims': 'http://iec.ch/TC57/1999/rdf-schema-extensions-19990926#'
    }

    classes = []
    enums = []
    enum_values = []
    properties = []

    for desc in root.findall('rdf:Description', ns):
        about = desc.attrib.get(f'{{{ns["rdf"]}}}about')
        if not about:
            continue

        label_el = desc.find('rdfs:label', ns)
        label = label_el.text.strip() if label_el is not None else about.split("#")[-1]
        stereotype = desc.find('cims:stereotype', ns)
        type_el = desc.find('rdf:type', ns)

        if stereotype is not None and "enumeration" in stereotype.attrib.get(f'{{{ns["rdf"]}}}resource', ''):
            enums.append(label)

        elif type_el is not None and any(e in type_el.attrib.get(f'{{{ns["rdf"]}}}resource', '') for e in enums):
            enum_values.append((label, type_el.attrib.get(f'{{{ns["rdf"]}}}resource', '').split("#")[-1]))

        elif type_el is not None and "rdf-schema#Property" in type_el.attrib.get(f'{{{ns["rdf"]}}}resource', ''):
            domain = desc.find('rdfs:domain', ns)
            range_ = desc.find('rdfs:range', ns)
            properties.append({
                "name": label,
                "domain": domain.attrib.get(f'{{{ns["rdf"]}}}resource', '').split("#")[-1] if domain is not None else None,
                "range": range_.attrib.get(f'{{{ns["rdf"]}}}resource', '').split("#")[-1] if range_ is not None else None
            })
        else:
            classes.append(label)

    return classes, enums, enum_values, properties


def generate_turtle(classes, enums, enum_values, properties):
    turtle = []
    turtle.append("""@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dbpedia: <http://dbpedia.org/resource/> .
@prefix dbo: <http://dbpedia.org/ontology/> .
@prefix dbp: <http://dbpedia.org/property/> .
@prefix tto: <http://example.org/ecommerce/ontology#> .
@prefix ttr: <http://example.org/ecommerce/resource#> .
@prefix prod: <http://iec.ch/TC57/prodaja#> .

# =====================================================
# CLASSES
# =====================================================
""")

    for c in classes:
        turtle.append(f"""tto:{c}
\trdf:type rdfs:Class;
\trdfs:label "{c.replace('_', ' ')}"^^xsd:string;
\trdfs:isDefinedBy tto: .\n""")

    if enums:
        turtle.append("# =====================================================\n# ENUMERATIONS\n# =====================================================\n")
        for e in enums:
            turtle.append(f"""tto:{e}
\trdf:type rdfs:Class;
\trdfs:label "{e.replace('_', ' ')}"^^xsd:string;
\trdfs:isDefinedBy tto: .\n""")

    if enum_values:
        turtle.append("# =====================================================\n# ENUM VALUES\n# =====================================================\n")
        for name, parent in enum_values:
            turtle.append(f"ttr:{name.upper()} rdf:type tto:{parent} .")

    if properties:
        turtle.append("\n# =====================================================\n# PROPERTIES\n# =====================================================\n")
        for prop in properties:
            label = prop["name"].replace('_', ' ')
            domain = prop["domain"]
            range_ = prop["range"]
            domain_str = f"rdfs:domain tto:{domain};" if domain else ""
            range_str = f"rdfs:range xsd:{range_.lower() if range_ else 'string'};" if range_ else ""
            turtle.append(f"""tto:{prop["name"]}
\trdf:type rdf:Property;
\trdfs:label "{label}"^^xsd:string;
\t{domain_str}
\t{range_str}
\trdfs:isDefinedBy tto: .\n""")

    return "\n".join(turtle)


def convert(xml_file, output_file=None):
    classes, enums, enum_values, properties = parse_rdfs(xml_file)
    ttl_data = generate_turtle(classes, enums, enum_values, properties)

    if not output_file:
        base, _ = os.path.splitext(xml_file)
        output_file = base + ".ttl"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(ttl_data)

    print(f"Ontology generated: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rdfs_to_turtle.py input_file.xml [output_file.ttl]")
        sys.exit(1)

    xml_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    convert(xml_file, output_file)
