"""
Generate sample XML files for testing
Different structures - simple, nested, with attributes, namespaces
"""

import os

os.makedirs('data/xml', exist_ok=True)

# 1. Books catalog 
books_xml = """<?xml version="1.0" encoding="UTF-8"?>
<catalog>
    <book id="bk101" category="Computer">
        <author>Gambardella, Matthew</author>
        <title>XML Developer's Guide</title>
        <price currency="USD">44.95</price>
        <publish_date>2000-10-01</publish_date>
        <description>An in-depth look at creating applications with XML.</description>
    </book>
    <book id="bk102" category="Fantasy">
        <author>Ralls, Kim</author>
        <title>Midnight Rain</title>
        <price currency="USD">5.95</price>
        <publish_date>2000-12-16</publish_date>
        <description>A former architect battles corporate zombies.</description>
    </book>
    <book id="bk103" category="Fantasy">
        <author>Corets, Eva</author>
        <title>Maeve Ascendant</title>
        <price currency="USD">5.95</price>
        <publish_date>2000-11-17</publish_date>
        <description>After the collapse of a nanotechnology society.</description>
    </book>
    <book id="bk104" category="Romance">
        <author>Corets, Eva</author>
        <title>Oberon's Legacy</title>
        <price currency="USD">5.95</price>
        <publish_date>2001-03-10</publish_date>
        <description>In post-apocalypse England, a young man searches.</description>
    </book>
    <book id="bk105" category="Computer">
        <author>O'Brien, Tim</author>
        <title>Microsoft .NET</title>
        <price currency="USD">49.95</price>
        <publish_date>2000-12-09</publish_date>
        <description>Microsoft's .NET initiative is explored in detail.</description>
    </book>
</catalog>
"""

with open('data/xml/books.xml', 'w', encoding='utf-8') as f:
    f.write(books_xml)
print("Created books.xml")

# 2. Employee records 
employees_xml = """<?xml version="1.0" encoding="UTF-8"?>
<company>
    <department name="Engineering">
        <employee id="E001">
            <name>John Doe</name>
            <position>Senior Engineer</position>
            <salary>95000</salary>
            <contact>
                <email>john.doe@company.com</email>
                <phone>555-0101</phone>
            </contact>
            <skills>
                <skill>Python</skill>
                <skill>Java</skill>
                <skill>SQL</skill>
            </skills>
        </employee>
        <employee id="E002">
            <name>Jane Smith</name>
            <position>Tech Lead</position>
            <salary>110000</salary>
            <contact>
                <email>jane.smith@company.com</email>
                <phone>555-0102</phone>
            </contact>
            <skills>
                <skill>JavaScript</skill>
                <skill>React</skill>
                <skill>Node.js</skill>
            </skills>
        </employee>
    </department>
    <department name="Sales">
        <employee id="E003">
            <name>Bob Johnson</name>
            <position>Sales Manager</position>
            <salary>85000</salary>
            <contact>
                <email>bob.j@company.com</email>
                <phone>555-0103</phone>
            </contact>
            <skills>
                <skill>Negotiation</skill>
                <skill>CRM</skill>
            </skills>
        </employee>
    </department>
</company>
"""

with open('data/xml/employees.xml', 'w', encoding='utf-8') as f:
    f.write(employees_xml)
print("Created employees.xml")

# 3. Product inventory 
products_xml = """<?xml version="1.0" encoding="UTF-8"?>
<inv:inventory xmlns:inv="http://example.com/inventory" xmlns:prod="http://example.com/products">
    <prod:product inv:id="P001" inv:inStock="true">
        <prod:name>Laptop</prod:name>
        <prod:category>Electronics</prod:category>
        <prod:price>999.99</prod:price>
        <prod:stock>45</prod:stock>
        <prod:supplier>TechSupply Inc</prod:supplier>
    </prod:product>
    <prod:product inv:id="P002" inv:inStock="true">
        <prod:name>Mouse</prod:name>
        <prod:category>Accessories</prod:category>
        <prod:price>25.99</prod:price>
        <prod:stock>150</prod:stock>
        <prod:supplier>PeripheralsPro</prod:supplier>
    </prod:product>
    <prod:product inv:id="P003" inv:inStock="false">
        <prod:name>Keyboard</prod:name>
        <prod:category>Accessories</prod:category>
        <prod:price>79.99</prod:price>
        <prod:stock>0</prod:stock>
        <prod:supplier>PeripheralsPro</prod:supplier>
    </prod:product>
</inv:inventory>
"""

with open('data/xml/products.xml', 'w', encoding='utf-8') as f:
    f.write(products_xml)
print("Created products.xml")

# 4. RSS feed example (real-world use case)
rss_xml = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Tech News Daily</title>
        <link>http://technews.example.com</link>
        <description>Latest technology news and updates</description>
        <item>
            <title>AI Breakthrough in 2024</title>
            <link>http://technews.example.com/ai-breakthrough</link>
            <pubDate>Mon, 01 Dec 2024 10:00:00 GMT</pubDate>
            <description>New AI model achieves human-level performance</description>
            <category>Artificial Intelligence</category>
        </item>
        <item>
            <title>Cloud Computing Trends</title>
            <link>http://technews.example.com/cloud-trends</link>
            <pubDate>Sun, 30 Nov 2024 15:30:00 GMT</pubDate>
            <description>Top cloud computing trends for next year</description>
            <category>Cloud</category>
        </item>
        <item>
            <title>Cybersecurity Alert</title>
            <link>http://technews.example.com/security-alert</link>
            <pubDate>Sat, 29 Nov 2024 08:45:00 GMT</pubDate>
            <description>New vulnerability discovered in popular framework</description>
            <category>Security</category>
        </item>
    </channel>
</rss>
"""

with open('data/xml/news_feed.xml', 'w', encoding='utf-8') as f:
    f.write(rss_xml)
print("Created news_feed.xml")

print("\n" + "="*50)
print("XML files created successfully!")
print("="*50)
print("\nFiles:")
print("1. data/xml/books.xml (simple with attributes)")
print("2. data/xml/employees.xml (nested structure)")
print("3. data/xml/products.xml (with namespaces)")
print("4. data/xml/news_feed.xml (RSS feed format)")
print("\nReady for xml_processing.py!")