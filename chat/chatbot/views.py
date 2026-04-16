import os
import shutil
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .services import process_pdf, ask_question, analyze_image_with_vlm, process_image_as_document
from django.views.decorators.csrf import csrf_exempt

CHROMA_DIR = "./chroma_db"

def index(request):
    return render(request, 'chatbot/index.html')

@csrf_exempt
def upload_document(request):
    if request.method == 'POST' and request.FILES.get('doc_file'):
        file = request.FILES['doc_file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        filepath = fs.path(filename)

        try:
            ext = os.path.splitext(filename)[1].lower()
            
            if ext == '.pdf':
                process_pdf(filepath)
                msg = "PDF indexé."
            elif ext in ['.jpg', '.jpeg', '.png']:
                process_image_as_document(filepath)
                msg = "Image de support indexée."
            else:
                return JsonResponse({"status": "error", "message": "Format non supporté."})
                
            return JsonResponse({"status": "success", "message": msg})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Aucun fichier reçu."})

@csrf_exempt
def chat_ask(request):
    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        image_file = request.FILES.get('image_file')
        
        if question or image_file:
            try:
                history = request.session.get('chat_history', [])
                formatted_history = "\n".join(history)
                
                final_input = question
                
                if image_file:
                    fs = FileSystemStorage()
                    filename = fs.save(image_file.name, image_file)
                    filepath = fs.path(filename)
                    
                    # Transcription Llava (Late Binding)
                    transcription = analyze_image_with_vlm(filepath)
                    
                    final_input = f"[IMAGE CONTENU : {transcription}]\n\nQuestion : {question}"
                    
                    if os.path.exists(filepath):
                        os.remove(filepath)

                answer = ask_question(final_input, short_history=formatted_history)
                
                history.append(f"Utilisateur: {question if question else '[Image]'}")
                history.append(f"IA: {answer}")
                request.session['chat_history'] = history[-6:]
                
                return JsonResponse({"answer": answer})
            except Exception as e:
                return JsonResponse({"answer": f"Error: {str(e)}"})
                
    return JsonResponse({"status": "error", "message": "Pas de question ou d'image reçue."})

@csrf_exempt
def clear_db(request):
    if request.method == 'POST':
        if 'chat_history' in request.session:
            del request.session['chat_history']

        if os.path.exists(CHROMA_DIR):
            shutil.rmtree(CHROMA_DIR)
            return JsonResponse({"message": "Database and sessions cleared."})
        return JsonResponse({"message": "Database already empty."})