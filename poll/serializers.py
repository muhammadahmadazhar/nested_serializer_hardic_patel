from rest_framework import serializers
from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        required=False
    )#its not need to write but if you want in validated_data its validity
    # must be checked if you explicity write like above
    #if you dont write id update will not work
    class Meta:
        model = Choice
        fields = [
            "id",
            "question",
            "text",
        ]
        read_only_fields = ('question',)
        # depth=1 #It will give parent table information too
        # depth=2 #It will give parent of parent table information too

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "title",
            "status",
            "created_by",
            "choices",
        ]
    def create(self, validated_data):
        # url=http://127.0.0.1:8000/api/questions/
        choices = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        # Choice.objects.create(question=question)
        for choice in choices:
            Choice.objects.create(**choice, question=question)
        return question

    def update(self, instance, validated_data):
        # url=http://127.0.0.1:8000/api/questions/7/
        choices = validated_data.pop('choices')
        instance.title = validated_data.get("title", instance.title)
        #if title is not passed from validated data then we get the same title which is in db
        print("instance.title",instance.title)
        instance.save()
        keep_choices = []
        existing_ids = [c.id for c in instance.choices]
        for choice in choices:
            if "id" in choice.keys():#seperate that choice which have id so we can update it
                if Choice.objects.filter(id=choice["id"]).exists():
                    #if given id is wrong then we dont need to update it instead add it as new
                    c = Choice.objects.get(id=choice["id"])
                    c.text = choice.get('text', c.text)
                    # if text is not passed from validated data then we get the same text which is in db
                    c.save()
                    keep_choices.append(c.id)
                else:
                    continue
            else:#seperate that choice which have only text so we can add new
                c = Choice.objects.create(**choice, question=instance)
                keep_choices.append(c.id)

        for choice in instance.choices:
            if choice.id not in keep_choices:
                choice.delete()

        return instance

# q = QuestionSerializer(data={"title": "How are you?"})
# q.errors
# q.data
