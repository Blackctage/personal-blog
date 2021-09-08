from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse  # To generate URLS by reversing URL patterns
from django.db import models


class ArticlesType(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )
    article_type_header = models.ForeignKey('ArticleTypeHeader', on_delete=models.RESTRICT, null=True)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Stories(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='stories_file')

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    publish_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Post(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    photo_or_video = models.FileField(upload_to='post_file', null=True)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    imprint = models.TextField(null=True)
    articles_type = models.ForeignKey('ArticlesType', on_delete=models.RESTRICT, null=True)
    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    publish_date = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('h', 'Hidden'),
        ('a', 'Available'),
        ('l', 'Look'),

    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book availability')

    class Meta:
        ordering = ['title']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('post-detail', args=[str(self.id)])


class Work(models.Model):
    photo = models.ImageField(upload_to='work_photos', null=True)
    second_photo = models.ImageField(upload_to='work_photos', null=True)
    title = models.CharField(max_length=50, help_text='Websites title')
    description = models.TextField(max_length=500, help_text='Websites description')
    tags = TaggableManager()
    link = models.URLField(null=True, help_text='Websites link')

    class Meta:
        ordering = ['title']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_update_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('work-update', args=[str(self.id)])

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('works')


class ArticleTypeHeader(models.Model):
    title = models.CharField(max_length=50)
    link = models.CharField(help_text='name for website link ', max_length=50)

    class Meta:
        ordering = ['title']

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80, null=True)
    profile_photo = models.ImageField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.body[:60]