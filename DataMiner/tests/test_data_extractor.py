from data_extractor import DataExtractor


HTML = """
<article class="product-card"><h2 class="product-name">  Widget </h2><span class="product-price">$12.50</span><span class="product-category"> tools </span><span class="product-availability">In Stock</span></article>
<article class="product-card"><h2 class="product-name">Broken</h2><span class="product-price">$1</span></article>
"""


def test_extracts_complete_product_cards():
    assert DataExtractor().extract(HTML) == [{"name": "Widget", "price": "$12.50", "category": "tools", "availability": "In Stock"}]


def test_malformed_cards_are_skipped_safely():
    assert DataExtractor().extract("<article class='product-card'><h2 class='product-name'>Only name</h2></article>") == []
