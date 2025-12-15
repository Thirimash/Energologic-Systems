"""
Services app models for OZE Website.
Contains ServicePage with StreamField for flexible content building.
"""
from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail import blocks


class PricingItemBlock(blocks.StructBlock):
    """Single pricing item."""
    name = blocks.CharBlock(max_length=100, label="Nazwa usługi")
    price = blocks.CharBlock(max_length=50, label="Cena")
    description = blocks.TextBlock(required=False, label="Opis")
    
    class Meta:
        icon = 'tag'
        label = 'Pozycja cennika'


class PricingTableBlock(blocks.StructBlock):
    """Pricing table section."""
    title = blocks.CharBlock(max_length=100, default="Cennik")
    items = blocks.ListBlock(PricingItemBlock())
    
    class Meta:
        icon = 'table'
        label = 'Cennik'
        template = 'services/blocks/pricing_table.html'


class GalleryBlock(blocks.StructBlock):
    """Image gallery section."""
    title = blocks.CharBlock(max_length=100, default="Galeria")
    images = blocks.ListBlock(ImageChooserBlock())
    
    class Meta:
        icon = 'image'
        label = 'Galeria'
        template = 'services/blocks/gallery.html'


class FAQItemBlock(blocks.StructBlock):
    """Single FAQ item."""
    question = blocks.CharBlock(max_length=200, label="Pytanie")
    answer = blocks.RichTextBlock(label="Odpowiedź")
    
    class Meta:
        icon = 'help'
        label = 'FAQ'


class FAQBlock(blocks.StructBlock):
    """FAQ section."""
    title = blocks.CharBlock(max_length=100, default="Często zadawane pytania")
    items = blocks.ListBlock(FAQItemBlock())
    
    class Meta:
        icon = 'help'
        label = 'Sekcja FAQ'
        template = 'services/blocks/faq.html'


class ServicePage(Page):
    """
    Service detail page with flexible StreamField content.
    Supports rich text, pricing tables, galleries, and FAQs.
    """
    
    # Basic info
    icon = models.CharField(
        max_length=50,
        default="sun",
        help_text="Heroicons name (e.g., 'sun', 'bolt', 'wrench')"
    )
    short_description = models.CharField(
        max_length=200,
        help_text="Krótki opis wyświetlany na stronie głównej"
    )
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Główne zdjęcie usługi"
    )
    
    # Flexible content
    content = StreamField([
        ('heading', blocks.CharBlock(
            max_length=200,
            icon='title',
            template='services/blocks/heading.html'
        )),
        ('paragraph', blocks.RichTextBlock(
            icon='doc-full',
            template='services/blocks/paragraph.html'
        )),
        ('image', ImageChooserBlock(
            icon='image',
            template='services/blocks/image.html'
        )),
        ('pricing', PricingTableBlock()),
        ('gallery', GalleryBlock()),
        ('faq', FAQBlock()),
    ], blank=True, use_json_field=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('icon'),
        FieldPanel('short_description'),
        FieldPanel('featured_image'),
        FieldPanel('content'),
    ]
    
    class Meta:
        verbose_name = "Strona usługi"
        verbose_name_plural = "Strony usług"
