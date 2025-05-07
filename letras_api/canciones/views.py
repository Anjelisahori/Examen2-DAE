import lyricsgenius
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LetraCancion
from .serializers import LetraCancionSerializer
from .spotify_utils import get_album_cover  

# Tu clave de API de Genius
genius = lyricsgenius.Genius("h6OgD6DsaROmSYO0oELexoHTxf-VO0qQCtndsuvxPLyBdQma3hAQnVx1dxwqWjed")

# Inicializa el analizador VADER
analyzer = SentimentIntensityAnalyzer()

class LetraCancionViewSet(viewsets.ModelViewSet):
    queryset = LetraCancion.objects.all()
    serializer_class = LetraCancionSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        try:
            # Buscar la letra con Genius
            cancion = genius.search_song(instance.titulo, instance.autor)
            if cancion and cancion.lyrics:
                instance.letra = cancion.lyrics

                # IA: análisis de emoción con VADER
                sentiment_score = analyzer.polarity_scores(instance.letra)
                sentimiento = sentiment_score['compound']

                # Clasificación de emociones
                if sentimiento >= 0.5:
                    emocion = "Feliz"
                elif sentimiento > 0:
                    emocion = "Tranquila"
                elif sentimiento == 0:
                    emocion = "Neutral"
                elif sentimiento > -0.5:
                    emocion = "Triste"
                else:
                    emocion = "Muy triste"

                instance.emocion = emocion
                instance.puntaje = round(sentimiento, 2)
            else:
                instance.letra = "Letra no encontrada"
                instance.emocion = "Desconocido"
                instance.puntaje = 0
        except Exception as e:
            instance.letra = "Letra no encontrada"
            instance.emocion = "Desconocido"
            instance.puntaje = 0

        try:
            # Buscar portada en Spotify
            portada = get_album_cover(instance.titulo, instance.autor)
            if portada:
                instance.portada_url = portada
        except Exception as e:
            instance.portada_url = None

        instance.save()

    @action(detail=True, methods=['get'])
    def recomendaciones(self, request, pk=None):
        try:
            cancion = self.get_object()
            emocion_actual = cancion.emocion

            # Buscar otras canciones con la misma emoción, excluyendo esta misma
            similares = LetraCancion.objects.filter(emocion=emocion_actual).exclude(id=cancion.id)[:5]
            serializer = self.get_serializer(similares, many=True)
            return Response({
                "emocion": emocion_actual,
                "recomendaciones": serializer.data
            })
        except LetraCancion.DoesNotExist:
            return Response({"error": "Canción no encontrada"}, status=404)
