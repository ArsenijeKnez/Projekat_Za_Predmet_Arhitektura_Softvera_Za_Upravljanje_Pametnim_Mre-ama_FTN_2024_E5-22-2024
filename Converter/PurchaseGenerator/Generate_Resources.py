from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD
from datetime import date
from urllib.parse import quote

TTO = Namespace("http://example.org/purchase/ontology#")
TTR = Namespace("http://example.org/purchase/resource#")

g = Graph()
g.bind("tto", TTO)
g.bind("ttr", TTR)
g.bind("rdfs", RDFS)
g.bind("rdf", RDF)
g.bind("xsd", XSD)


korisnici = [
    (TTR["User1"], TTO["User"], "Marko Petrović", "marko@example.com", TTR["CUSTOMER"]),
    (TTR["User2"], TTO["User"], "Ana Jovanović", "ana@example.com", TTR["ADMIN"]),
]

for korisnik, rdf_class, ime, email, uloga in korisnici:
    g.add((korisnik, RDF.type, rdf_class))
    g.add((korisnik, TTO["userId"], Literal(int(korisnik.split("#User")[1]))))
    g.add((korisnik, TTO["name"], Literal(ime)))
    g.add((korisnik, TTO["email"], Literal(email)))
    g.add((korisnik, TTO["hasRole"], uloga))

proizvodi = [
    (TTR["Product1"], "Proizvod 1", 59.99, TTR["Inventory1"]),
    (TTR["Product2"], "Proizvod 2", 129.50, TTR["Inventory2"]),
]

for proizvod, naziv, cena, inventar in proizvodi:
    g.add((proizvod, RDF.type, TTO["Product"]))
    g.add((proizvod, TTO["productId"], Literal(int(proizvod.split("#Product")[1]))))
    g.add((proizvod, RDFS.label, Literal(naziv)))
    g.add((proizvod, TTO["price"], Literal(cena, datatype=XSD.float)))
    g.add((proizvod, TTO["manages"], inventar))

inventari = [
    (TTR["Inventory1"], 5001, 15),
    (TTR["Inventory2"], 5002, 7),
]
for inventar, inv_id, kolicina in inventari:
    g.add((inventar, RDF.type, TTO["Inventory"]))
    g.add((inventar, TTO["inventoryId"], Literal(inv_id)))
    g.add((inventar, TTO["quantity"], Literal(kolicina)))

narudzbine = [
    (TTR["Order1"], 9001, date.today().isoformat(), TTR["Product1"], TTR["Shipping1"], TTR["Payment1"], TTR["Discount1"], TTR["COMPLETED"]),
]
for order, oid, datum, proizvod, isporuka, uplata, popust, status in narudzbine:
    g.add((order, RDF.type, TTO["Order"]))
    g.add((order, TTO["orderId"], Literal(oid)))
    g.add((order, TTO["orderDate"], Literal(datum, datatype=XSD.date)))
    g.add((order, TTO["contains"], proizvod))
    g.add((order, TTO["ships"], isporuka))
    g.add((order, TTO["processes"], uplata))
    g.add((order, TTO["applies"], popust))
    g.add((order, TTO["hasStatus"], status))

placanja = [
    (TTR["Payment1"], 3001, 59.99, TTR["CREDIT_CARD"]),
]
for uplata, pid, iznos, metoda in placanja:
    g.add((uplata, RDF.type, TTO["Payment"]))
    g.add((uplata, TTO["paymentId"], Literal(pid)))
    g.add((uplata, TTO["amount"], Literal(iznos, datatype=XSD.float)))
    g.add((uplata, TTO["hasMethod"], metoda))

g.add((TTR["Shipping1"], RDF.type, TTO["Shipping"]))
g.add((TTR["Shipping1"], TTO["shippingId"], Literal(7001)))
g.add((TTR["Shipping1"], TTO["address"], Literal("Bulevar Oslobođenja 12, Novi Sad")))

g.add((TTR["Review1"], RDF.type, TTO["Review"]))
g.add((TTR["Review1"], TTO["reviewId"], Literal(4001)))
g.add((TTR["Review1"], TTO["rating"], Literal(5)))
g.add((TTR["Product1"], TTO["receivesReview"], TTR["Review1"]))
g.add((TTR["User1"], TTO["writes"], TTR["Review1"]))

notifikacije = [
    (TTR["Notif1"], 8001, "Vaša narudžbina je uspešno plaćena i poslata."),
    (TTR["Notif2"], 8002, "Sistem obaveštenje: Nova recenzija dodata."),
]
for notif, nid, poruka in notifikacije:
    g.add((notif, RDF.type, TTO["Notification"]))
    g.add((notif, TTO["notificationId"], Literal(nid)))
    g.add((notif, TTO["message"], Literal(poruka)))

g.add((TTR["Discount1"], RDF.type, TTO["Discount"]))
g.add((TTR["Discount1"], TTO["discountId"], Literal(6001)))
g.add((TTR["Discount1"], TTO["percentage"], Literal(10.0, datatype=XSD.float)))


g.add((TTR["User1"], TTO["places"], TTR["Order1"]))
g.add((TTR["User1"], TTO["receivesNotification"], TTR["Notif1"]))
g.add((TTR["User2"], TTO["receivesNotification"], TTR["Notif2"]))

g.serialize("resources.ttl", format="turtle")
print("'resources.ttl' uspešno generisan!")
