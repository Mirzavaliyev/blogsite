from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,  # Bir xil nomli kategoriyalarni oldini olish
        verbose_name="Kategoriya nomi",
        help_text="Postning kategoriyasi"  # Admin panelda ko'rsatiladigan yordam matni
    )

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']  # Kategoriyalar alifbo bo'yicha tartiblansin

    def __str__(self):
        return self.name or "Nomsiz kategoriya"  # name=None bo'lsa ham ishlaydi


class Post(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Sarlavha",
        help_text="Postning sarlavhasi"
    )
    content = models.TextField(
        verbose_name="Mazmuni",
        help_text="Postning asosiy matni"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqt"
    )
    views_count = models.IntegerField(
        default=0,
        verbose_name="Ko'rishlar:",
        editable=False  # Admin panelda tahrirlanmasin
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # Kategoriya o'chirilsa, post o'chmasin
        related_name='posts',
        null=True,
        blank=True,
        verbose_name="Kategoriya"
    )

    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        # Sarlavha o‘zgarganda slug’ni yangilash
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while Post.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Postlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    ip_address = models.CharField(max_length=45)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together =('post', 'ip_address')

        def __str__(self):
            return f"{self.ip_address} viewed {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Post"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Muallif"
    )
    content = models.TextField(
        verbose_name="Izoh matni",
        help_text="Foydalanuvchi izohi"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqt"
    )

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ['-created_at']  # Eng yangi izohlar yuqorida

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"
