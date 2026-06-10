from rest_framework import serializers
from django.contrib.auth import get_user_model

# Pega o modelo customizado que foi criado para o usuário, garantindo que estamos usando o modelo correto mesmo que ele seja personalizado
User = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    # Definindo o  write_only=True para que a senha nunca seja retornada na resposta da API
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_lojista']

    def create(self, validated_data):
        # O método create_user é fundamental aqui, pois ele criptografa (faz o hash) da senha automaticamente
        user = User.objects.create_user(
            username=validated_data.get('username', ''),
            email=validated_data['email'],
            password=validated_data['password'],
            is_lojista=validated_data.get('is_lojista', False)
        )
        return user