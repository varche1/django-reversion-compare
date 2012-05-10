# coding: utf-8

from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SimpleModel(models.Model):
    text = models.CharField(max_length=255)


class ParentModel(models.Model):
    parent_name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.parent_name


class ChildModel(ParentModel):
    child_name = models.CharField(max_length=255)
    file = models.FileField(upload_to="test", blank=True)
    genericrelatedmodel_set = GenericRelation("reversion_compare_test_app.GenericRelatedModel")

    def __unicode__(self):
        return u"%s > %s" % (self.parent_name, self.child_name)

    class Meta:
        verbose_name = _("child model")
        verbose_name_plural = _("child models")


class RelatedModel(models.Model):
    child_model = models.ForeignKey(ChildModel)
    related_name = models.CharField(max_length=255)
    file = models.FileField(upload_to="test", blank=True)

    def __unicode__(self):
        return self.related_name


class GenericRelatedModel(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.TextField()
    child_model = GenericForeignKey()
    generic_related_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.generic_related_name


class FlatExampleModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, blank=True, null=True)
    content = models.TextField(help_text="Here is a content text field and this line is the help text from the model field.")
    child_model = models.ForeignKey(ChildModel, blank=True, null=True)

#------------------------------------------------------------------------------

class HobbyModel(models.Model):
    name = models.CharField(max_length=128)
    def __unicode__(self):
        return "Hobby '%s'" % self.name


class PersonModel(models.Model):
    name = models.CharField(max_length=128)
    friends = models.ManyToManyField("self", blank=True, null=True)
    hobbies = models.ManyToManyField(HobbyModel, blank=True, null=True)
    def __unicode__(self):
        return "Person '%s'" % self.name


class GroupModel(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(PersonModel, through='MembershipModel')
    def __unicode__(self):
        return "'%s' group" % self.name


class MembershipModel(models.Model):
    person = models.ForeignKey(PersonModel)
    group = models.ForeignKey(GroupModel)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
    def __unicode__(self):
        return "Person '%s' member of '%s' group" % (self.person.name, self.group.name)
