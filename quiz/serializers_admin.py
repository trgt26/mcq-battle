# serializers.py
from rest_framework import serializers
from .models import Question, QuestionSet, AnswerSet, QuestionQuestionSetMapper

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # fields = '__all__'
        fields = ['id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']

class QuestionQuestionSetMapperSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = QuestionQuestionSetMapper
        fields = ['id', 'question', 'order']

class QuestionSetSerializer(serializers.ModelSerializer):
    # mappings = QuestionQuestionSetMapperSerializer(many=True, read_only=True)
    mappings =  QuestionQuestionSetMapperSerializer(source='questionquestionsetmapper_set', many=True)
    # text = QuestionSerializer(many = True)
    class Meta:
        model = QuestionSet
        fields = '__all__'
        # fields = [ 'id', 'mappings']

class QuestionSetUpdateSerializer(serializers.ModelSerializer):
    question_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, 
        required = False
    )
    name = serializers.CharField(required=False)
    class Meta:
        model = QuestionSet
        fields = ['id', 'name', 'question_ids']

    def update(self, instance, validated_data):
        question_ids = validated_data.pop('question_ids', None)
        name = validated_data.get('name')
        
        if question_ids is not None:
            # Clear existing mappings for the questionset
            QuestionQuestionSetMapper.objects.filter(question_set=instance).delete()

            # Create new mappings with the provided question IDs
            for order, question_id in enumerate(question_ids, start=1):
                QuestionQuestionSetMapper.objects.create(
                    question_id=question_id,
                    question_set=instance,
                    order=order
                )

            # Update the other fields of the QuestionSet instance
            instance.name = validated_data.get('name', instance.name)
            instance.save()
        if name is not None:
            instance.name = name
            instance.save()
        return instance

class QuestionSetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSet
        fields = '__all__'

class AnswerSetSerializer(serializers.ModelSerializer):
    question_set = QuestionSetSerializer(many=True)

    class Meta:
        model = AnswerSet
        fields = '__all__'
