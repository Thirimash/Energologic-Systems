"""
Home app models for OZE Website.
Contains HomePage with hero section, services grid, and partners carousel.
"""
from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page, Orderable
from wagtail import blocks


class WhyUsBlock(blocks.StructBlock):
    """Block for 'Why Us' section with icon, title, and description."""
    icon = blocks.CharBlock(
        max_length=50,
        help_text="Heroicons name (e.g., 'shield-check', 'clock', 'currency-dollar')"
    )
    title = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock()

    class Meta:
        icon = 'tick'
        label = 'Dlaczego my - element'


class HomePage(Page):
    """
    Main landing page for OZE Website.
    Includes hero section, 'Why Us' section, services grid, and partners.
    """
    
    # Hero Section
    hero_title = models.CharField(
        max_length=200,
        default="Profesjonalne przeglądy instalacji fotowoltaicznych"
    )
    hero_subtitle = models.CharField(
        max_length=300,
        default="Zapewniamy bezpieczeństwo i maksymalną wydajność Twojej instalacji PV"
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Zdjęcie w tle sekcji hero"
    )
    hero_cta_text = models.CharField(
        max_length=50,
        default="Zamów przegląd"
    )
    hero_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Link do strony po kliknięciu CTA"
    )
    
    # Why Us Section
    why_us_title = models.CharField(
        max_length=100,
        default="Dlaczego my?"
    )
    why_us_items = StreamField(
        [('item', WhyUsBlock())],
        blank=True,
        use_json_field=True
    )
    
    # Services Section
    services_title = models.CharField(
        max_length=100,
        default="Nasze usługi"
    )
    services_subtitle = models.CharField(
        max_length=200,
        default="Kompleksowa obsługa instalacji OZE"
    )
    
    # Partners Section
    partners_title = models.CharField(
        max_length=100,
        default="Zaufali nam"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_image'),
            FieldPanel('hero_cta_text'),
            FieldPanel('hero_cta_link'),
        ], heading="Sekcja Hero"),
        MultiFieldPanel([
            FieldPanel('why_us_title'),
            FieldPanel('why_us_items'),
        ], heading="Sekcja Dlaczego My"),
        MultiFieldPanel([
            FieldPanel('services_title'),
            FieldPanel('services_subtitle'),
        ], heading="Sekcja Usługi"),
        MultiFieldPanel([
            FieldPanel('partners_title'),
            InlinePanel('partner_logos', label="Logo partnera"),
        ], heading="Sekcja Partnerzy"),
    ]
    
    def get_services(self):
        """Return all published ServicePage instances."""
        from apps.services.models import ServicePage
        return ServicePage.objects.live().order_by('title')
    
    class Meta:
        verbose_name = "Strona główna"


class PartnerLogo(Orderable):
    """Partner logo for the partners carousel."""
    page = ParentalKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name='partner_logos'
    )
    name = models.CharField(max_length=100)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    website = models.URLField(blank=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('website'),
    ]
