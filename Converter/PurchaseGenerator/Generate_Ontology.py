from rdflib import Graph, Namespace, RDF, RDFS, XSD, Literal, URIRef

#Generate ontology for Purchase
g = Graph()

#Namespaces
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
dbpedia = Namespace("http://dbpedia.org/resource/")
dbo = Namespace("http://dbpedia.org/ontology/")
dbp = Namespace("http://dbpedia.org/property/")
tto = Namespace("http://example.org/purchase/ontology#")
ttr = Namespace("http://example.org/purchase/resource#")
prod = Namespace("http://iec.ch/TC57/purchase#")
g.bind("xsd", xsd)
g.bind("rdf", rdf)
g.bind("rdfs", rdfs)
g.bind("dbpedia", dbpedia)
g.bind("dbo", dbo)
g.bind("dbp", dbp)
g.bind("tto", tto)
g.bind("ttr", ttr)
g.bind("prod", prod)

#classes and enumerations
classes = [
    "User", "Product", "Order", "Payment", "ShoppingCart", "Inventory",
    "Shipping", "Review", "Notification", "Discount",
    "OrderStatus", "PaymentMethod", "UserRole"
]

for c in classes:
    g.add((tto[c], RDF.type, RDFS.Class))
    g.add((tto[c], RDFS.label, Literal(c, datatype=XSD.string)))
    g.add((tto[c], RDFS.isDefinedBy, URIRef(str(tto))))


enum_values = {
    "OrderStatus": ["PENDING", "COMPLETED", "CANCELLED"],
    "PaymentMethod": ["CREDIT_CARD", "PAYPAL", "BANK_TRANSFER"],
    "UserRole": ["ADMIN", "CUSTOMER", "GUEST"]
}

for enum_class, values in enum_values.items():
    for v in values:
        g.add((ttr[v], RDF.type, tto[enum_class]))


data_properties = [
    ("userId", "User", XSD.int),
    ("name", "User", XSD.string),
    ("email", "User", XSD.string),

    ("productId", "Product", XSD.int),
    ("price", "Product", XSD.float),

    ("orderId", "Order", XSD.int),
    ("orderDate", "Order", XSD.date),

    ("paymentId", "Payment", XSD.int),
    ("amount", "Payment", XSD.float),

    ("inventoryId", "Inventory", XSD.int),
    ("quantity", "Inventory", XSD.int),

    ("shippingId", "Shipping", XSD.int),
    ("address", "Shipping", XSD.string),

    ("reviewId", "Review", XSD.int),
    ("rating", "Review", XSD.int),

    ("notificationId", "Notification", XSD.int),
    ("message", "Notification", XSD.string),

    ("discountId", "Discount", XSD.int),
    ("percentage", "Discount", XSD.float)
]

for prop, domain, range_ in data_properties:
    g.add((tto[prop], RDF.type, RDF.Property))
    g.add((tto[prop], RDFS.label, Literal(prop, datatype=XSD.string)))
    g.add((tto[prop], RDFS.domain, tto[domain]))
    g.add((tto[prop], RDFS.range, range_))
    g.add((tto[c], RDFS.isDefinedBy, URIRef(str(tto))))


object_properties = [
    ("places", "User", "Order"),
    ("processes", "Order", "Payment"),
    ("contains", "Order", "Product"),
    ("holds", "ShoppingCart", "Product"),
    ("manages", "Product", "Inventory"),
    ("ships", "Order", "Shipping"),
    ("writes", "User", "Review"),
    ("receivesReview", "Product", "Review"),
    ("receivesNotification", "User", "Notification"),
    ("applies", "Order", "Discount"),
    ("hasRole", "User", "UserRole"),
    ("hasStatus", "Order", "OrderStatus"),
    ("hasMethod", "Payment", "PaymentMethod")
]

for prop, domain, range_ in object_properties:
    g.add((tto[prop], RDF.type, RDF.Property))
    g.add((tto[prop], RDFS.label, Literal(prop, datatype=XSD.string)))
    g.add((tto[prop], RDFS.domain, tto[domain]))
    g.add((tto[prop], RDFS.range, tto[range_]))
    g.add((tto[c], RDFS.isDefinedBy, URIRef(str(tto))))

output_file = "ontology.ttl"
g.serialize(destination=output_file, format="turtle")
print(f"Ontology generated and saved to '{output_file}'")
