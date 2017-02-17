# coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from preferences.models import Preferences

from WEIPDCRM.models.release import Release


def validator_alias(value):
    if value[len(value) - 1:] != '/':
        raise ValidationError(_("Path alias should be suffixed by a slash char."))


class Setting(Preferences):
    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")
    active_release = models.ForeignKey(
        Release,
        verbose_name=_("Active Release"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Each repository should have an active release, otherwise it will not be "
                    "recognized by any advanced package tools.")
    )
    packages_compression = models.IntegerField(
        verbose_name=_("packages Compression"),
        choices=(
            (0, _("plain")),
            (1, _("gzip")),
            (2, _("plain and gzip")),
            (3, _("bzip")),
            (4, _("plain and bzip")),
            (5, _("gzip and bzip")),
            (6, _("all")),
        ),
        default=6,
        help_text=_(
            "Please change the compression method if error occurred when try to rebuild the list."
        )
    )
    packages_validation = models.IntegerField(
        verbose_name=_("Packages Validation"),
        choices=(
            (0, _("No validation")),
            (1, _("MD5Sum")),
            (2, _("MD5Sum & SHA1")),
            (3, _("MD5Sum & SHA1 & SHA256 (Recommended)")),
            (4, _("MD5Sum & SHA1 & SHA256 & SHA512")),
        ),
        default=1,
        help_text=_(
            "It will not take effect until any version edited or added."
        ),
    )
    downgrade_support = models.BooleanField(
        verbose_name=_("Downgrade Support"),
        help_text=_(
            "Allow multiple versions to exist in the latest package list."
        ),
        default=True
    )
    advanced_mode = models.BooleanField(
        verbose_name=_("Auto Depiction"),
        help_text=_(
            "Check it to generate awesome depiction page for each version."
        ),
        default=True
    )
    atomic_storage = models.BooleanField(
        verbose_name=_("Atomic Storage"),
        help_text=_(
            "Generate a new copy of package after editing control columns."
        ),
        default=False
    )
    resources_alias = models.CharField(
        verbose_name=_("Resources Alias"),
        help_text=_("You can specify alias for resources path in Nginx or "
                    "other HTTP servers, which is necessary for CDN speedup."),
        max_length=255,
        default="/resources/",
        validators=[
            validator_alias
        ]
    )

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,)
        )
