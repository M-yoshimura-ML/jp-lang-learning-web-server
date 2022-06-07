from rest_framework import serializers
from .models import Lesson, LessonContent, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LessonContentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = LessonContent
        fields = [
            'id',
            'lesson',
            'type',
            'content',
            'order_num'
        ]
        read_only_fields = ('lesson',)
        # depth=1


class LessonSerializer(serializers.ModelSerializer):
    contents = LessonContentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'description',
            'level',
            'contents'
        ]

    def create(self, validated_data):
        contents = validated_data.pop('contents')
        lesson = Lesson.objects.create(**validated_data)
        for content in contents:
            LessonContent.objects.create(**content, lesson=lesson)
        return lesson

    def update(self, instance, validated_data):
        contents = validated_data.pop('contents')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.level = validated_data.get('level', instance.level)
        instance.save()
        keep_contents = []
        existing_ids = [c.id for c in instance.contents]
        for content in contents:
            if 'id' in content.keys():
                if LessonContent.objects.filter(id=content['id']).exists():
                    c = LessonContent.objects.get(id=content['id'])
                    c.content = content.get('content', c.content)
                    c.save()
                    keep_contents.append(c.id)
                else:
                    continue
            else:
                c = LessonContent.objects.create(**content, lesson=instance)
                keep_contents.append(c.id)

        for content in instance.contents:
            if content.id not in keep_contents:
                content.delete()
        return instance

