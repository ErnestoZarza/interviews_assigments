from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# region Post Status Flags
DRAFT = 0
PUBLISHED = 1
HIDDEN = 2

# endregion


# region Group Status Flags
PRIVATE = 0
PUBLIC = 1

# endregion


# region Permissions Flags
CAN_EDIT_GROUP = 0
CAN_EDIT_POST = 1

CAN_CHANGE_STATUS_GROUP = 2
CAN_CHANGE_STATUS_POST = 3
CAN_CHANGE_STATUS_COMMENT = 4

CAN_DELETE_GROUP = 5
CAN_DELETE_POST = 6
CAN_DELETE_COMMENT = 7
CAN_DELETE_USER = 8


# endregion

# region User Model
class User(models.Model):
    """
       class that define a user(member) of the Group
    """
    name = models.CharField(_('name'), max_length=255)

    nickname = models.CharField(_('nickname'), max_length=255,
                                blank=True)

    email = models.EmailField(_('email'), blank=True)

    description = models.TextField(_('description'), blank=True)

    date_birthday = models.DateField(_('birthday'), null=True,
                                     blank=True)

    slug = models.SlugField(_('slug'), max_length=255,
                            unique=True,
                            help_text=_("Used to build the user's URL."))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


# endregion

# region Post Model Classes
class CorePost(models.Model):
    """
    class that define a post in the Group
    """
    STATUS_CHOICES = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
        (HIDDEN, _('Hidden'))
    )

    slug = models.SlugField(_('slug'), max_length=255,
                            help_text=_("Used for the Post's Url."))

    body = models.TextField(_('content'), blank=True)

    publication_date = models.DateTimeField(_('published'),
                                            db_index=True, default=timezone.now,
                                            help_text=_("Publication Date."))

    updated = models.DateTimeField(_('updated'), auto_now=True)

    status = models.IntegerField(_('status'), db_index=True,
                                 choices=STATUS_CHOICES, default=DRAFT)

    # I dismiss others fields like images etc

    class Meta:
        """
        Post's meta informations.
        """
        abstract = True

        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class AuthorPost(models.Model):
    authors = models.ForeignKey('User',
                                on_delete=models.CASCADE,
                                related_name='posts',
                                verbose_name=_('author'))

    class Meta:
        abstract = True


class Post(CorePost, AuthorPost):
    """
    Final model class for a Post representation
    """


# endregion

# region Comment Model Classes
class CoreComment(models.Model):
    """
       class that define a comment in a post
       """
    STATUS_CHOICES = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
        (HIDDEN, _('Hidden'))
    )

    content = models.TextField(_('comment'))

    submit_day = models.DateTimeField(_('date'), auto_now_add=True)

    ip = models.GenericIPAddressField(_('ip'))

    status = models.IntegerField(_('status'), db_index=True,
                                 choices=STATUS_CHOICES, default=DRAFT)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        abstract = True


class AuthorComment(models.Model):
    author = models.ForeignKey('User',
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name=_('author'))

    class Meta:
        abstract = True


class PostComment(models.Model):
    post = models.ForeignKey('Post',
                             on_delete=models.CASCADE,
                             verbose_name=_('post'),
                             related_name='comments')

    class Meta:
        abstract = True


class Comment(CoreComment, AuthorComment, PostComment):
    """"Final model class for a comment representation"""


# endregion

# region Group Model Classes
class CoreGroup(models.Model):
    """
        class that define a Group
        """
    STATUS_CHOICES = (
        (PRIVATE, _('Private')),
        (PUBLIC, _('Public'))
    )

    title = models.CharField(_('title'), max_length=255)

    description = models.TextField(_('description'), blank=True)

    slug = models.SlugField(_('slug'), max_length=255,
                            unique=True,
                            help_text=_("Used to build the author's URL."))

    created = models.DateTimeField(_('created'), auto_now_add=True)

    updated = models.DateTimeField(_('updated'), auto_now=True)

    status = models.IntegerField(_('status'), db_index=True,
                                 choices=STATUS_CHOICES, default=PUBLIC)

    class Meta:
        abstract = True
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class GroupMembers(models.Model):
    members = models.ManyToManyField('User',
                                     related_name='groups',
                                     verbose_name=_('members'))

    class Meta:
        abstract = True


class GroupAdministrators(models.Model):
    members = models.ManyToManyField('User',
                                     related_name='groups',
                                     verbose_name=_('administrators'))

    class Meta:
        abstract = True


class Group(CoreGroup, GroupAdministrators, GroupMembers):
    """
    Final model class for a Blog representation
    """

# endregion