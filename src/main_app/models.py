from django.db import models

# Create your models here.


class SoftDeleteMixinQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_soft_deleted=False)

    def purge(self):
        return super().delete()


class SoftDeleteMixinManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteMixinQuerySet(self.model, using=self._db).exclude(
            is_soft_deleted=True
        )

    def deleted(self):
        return SoftDeleteMixinQuerySet(self.model, using=self._db).filter(
            is_soft_deleted=True
        )

    def active(self):
        return self.get_queryset().filter(is_soft_deleted=False)

    def deactive(self):
        return self.get_queryset().filter(is_soft_deleted=True)

    def everything(self):
        return SoftDeleteMixinQuerySet(self.model, using=self._db)


class TimeStampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SoftDeleteMixin(models.Model):
    class Meta:
        abstract = True

    is_soft_deleted = models.BooleanField(default=False)
    objects = SoftDeleteMixinManager()

    def delete(self, *args, **kwargs):
        self.is_soft_deleted = True

        self.save()

    # def purge(self, using=None, keep_parents=False):
    #     return super().delete(using=using, keep_parents=keep_parents)


class ModelMixin(TimeStampMixin, SoftDeleteMixin):
    class Meta:
        abstract = True
