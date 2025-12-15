"""
Contact app models for OZE Website.
Contains ContactPage with Wagtail FormBuilder integration.
"""
from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField


class FormField(AbstractFormField):
    """Custom form field for ContactPage."""
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )


class ContactPage(AbstractEmailForm):
    """
    Contact page with Wagtail FormBuilder.
    Includes company information, map, and customizable form fields.
    """
    
    # Intro section
    intro = RichTextField(
        blank=True,
        help_text="Tekst wprowadzający nad formularzem"
    )
    thank_you_text = RichTextField(
        blank=True,
        help_text="Tekst wyświetlany po wysłaniu formularza"
    )
    
    # Company information
    company_name = models.CharField(max_length=200, blank=True)
    company_address = models.TextField(blank=True)
    company_phone = models.CharField(max_length=20, blank=True)
    company_email = models.EmailField(blank=True)
    company_nip = models.CharField(max_length=15, blank=True, verbose_name="NIP")
    
    # Map
    map_embed_url = models.URLField(
        blank=True,
        help_text="URL do osadzenia mapy Google Maps (iframe src)"
    )
    
    # Working hours
    working_hours = models.TextField(
        blank=True,
        help_text="Godziny pracy, np. 'Pon-Pt: 8:00-16:00'"
    )
    
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Pola formularza"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldPanel('company_name'),
            FieldPanel('company_address'),
            FieldPanel('company_phone'),
            FieldPanel('company_email'),
            FieldPanel('company_nip'),
            FieldPanel('working_hours'),
        ], heading="Dane firmy"),
        FieldPanel('map_embed_url'),
        MultiFieldPanel([
            FieldPanel('to_address'),
            FieldPanel('from_address'),
            FieldPanel('subject'),
        ], heading="Ustawienia email"),
    ]
    
    class Meta:
        verbose_name = "Strona kontaktowa"
