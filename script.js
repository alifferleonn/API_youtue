document.addEventListener('DOMContentLoaded', (event) => {
    const currentYearSpan = document.getElementById('currentYear');
    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }
    
    const titleForm = document.getElementById('titleForm');
    const titleListUl = document.getElementById('titleList');
    const titleStatusMessageDiv = document.getElementById('titleStatusMessage');
    const submitTitleButton = document.getElementById('submitTitleButton');

    const descriptionSectionDiv = document.getElementById('descriptionSection');
    const descriptionStatusMessageDiv = document.getElementById('descriptionStatusMessage');
    const generatedDescriptionDiv = document.getElementById('generatedDescription');
    const copyDescriptionButton = document.getElementById('copyDescriptionButton');

    let currentTopicForDesc = '';
    let currentKeywordsForDesc = '';

    if (titleForm) {
        titleForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            if (titleListUl) titleListUl.innerHTML = '';
            if (descriptionSectionDiv) descriptionSectionDiv.style.display = 'none'; 
            if (generatedDescriptionDiv) generatedDescriptionDiv.innerHTML = '';
            if (copyDescriptionButton) copyDescriptionButton.style.display = 'none';

            showStatusMessage(titleStatusMessageDiv, 'Gerando títulos, por favor aguarde...', 'loading');
            if (submitTitleButton) {
                submitTitleButton.disabled = true;
                submitTitleButton.textContent = 'Gerando Títulos... 🧠';
            }
            
            const topicInput = document.getElementById('topic');
            const keywordsInput = document.getElementById('keywords');
            if (topicInput) currentTopicForDesc = topicInput.value;
            if (keywordsInput) currentKeywordsForDesc = keywordsInput.value;

            const formData = new FormData(titleForm);
            const data = {
                topic: currentTopicForDesc,
                keywords: currentKeywordsForDesc,
                style: formData.get('style'),
                suggestions: parseInt(formData.get('suggestions'))
            };

            try {
                const response = await fetch('http://127.0.0.1:5000/generate-titles', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json',},
                    body: JSON.stringify(data),
                });

                hideStatusMessage(titleStatusMessageDiv);

                if (!response.ok) {
                    const errorResult = await response.json().catch(() => ({ error: `Erro HTTP: ${response.status}` }));
                    throw new Error(errorResult.error);
                }

                const result = await response.json();

                if (result.titles && result.titles.length > 0) {
                    result.titles.forEach(titleText => {
                        const listItem = document.createElement('li');
                        
                        const titleSpan = document.createElement('span');
                        titleSpan.textContent = titleText;
                        listItem.appendChild(titleSpan);

                        const descButton = document.createElement('button');
                        descButton.textContent = 'Gerar Descrição ✍️';
                        descButton.className = 'secondary-action';
                        descButton.type = 'button'; 
                        descButton.onclick = () => generateDescriptionForTitle(titleText);
                        listItem.appendChild(descButton);
                        
                        if (titleListUl) titleListUl.appendChild(listItem);
                    });
                } else if (result.error) {
                    throw new Error(result.error);
                } else {
                    showStatusMessage(titleStatusMessageDiv, 'Nenhum título foi gerado. Tente refinar sua busca.', 'error');
                }

            } catch (error) {
                console.error('Erro ao gerar títulos:', error);
                showStatusMessage(titleStatusMessageDiv, `Erro: ${error.message}`, 'error');
            } finally {
                if (submitTitleButton) {
                    submitTitleButton.disabled = false;
                    submitTitleButton.textContent = 'Gerar Títulos ✨';
                }
            }
        });
    }

    async function generateDescriptionForTitle(selectedTitle) {
        if (descriptionSectionDiv) descriptionSectionDiv.style.display = 'block';
        if (generatedDescriptionDiv) generatedDescriptionDiv.innerHTML = ''; 
        if (copyDescriptionButton) copyDescriptionButton.style.display = 'none';
        showStatusMessage(descriptionStatusMessageDiv, 'Gerando descrição, por favor aguarde...', 'loading');

        const dataForDesc = {
            title: selectedTitle,
            topic: currentTopicForDesc,
            keywords: currentKeywordsForDesc
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/generate-description', {
                method: 'POST',
                headers: {'Content-Type': 'application/json',},
                body: JSON.stringify(dataForDesc),
            });

            hideStatusMessage(descriptionStatusMessageDiv);

            if (!response.ok) {
                const errorResult = await response.json().catch(() => ({ error: `Erro HTTP: ${response.status}` }));
                throw new Error(errorResult.error);
            }

            const result = await response.json();

            if (result.description) {
                if (generatedDescriptionDiv) generatedDescriptionDiv.textContent = result.description; 
                if (copyDescriptionButton) copyDescriptionButton.style.display = 'inline-block';
            } else if (result.error) {
                throw new Error(result.error);
            } else {
                showStatusMessage(descriptionStatusMessageDiv, 'Não foi possível gerar a descrição.', 'error');
            }

        } catch (error) {
            console.error('Erro ao gerar descrição:', error);
            showStatusMessage(descriptionStatusMessageDiv, `Erro: ${error.message}`, 'error');
        }
    }
    
    if (copyDescriptionButton) {
        copyDescriptionButton.addEventListener('click', () => {
            const descriptionText = generatedDescriptionDiv ? generatedDescriptionDiv.textContent : '';
            if (descriptionText) {
                navigator.clipboard.writeText(descriptionText).then(() => {
                    const originalText = copyDescriptionButton.textContent;
                    copyDescriptionButton.textContent = 'Copiado!';
                    setTimeout(() => {
                        copyDescriptionButton.textContent = originalText;
                    }, 2000);
                }).catch(err => {
                    console.error('Falha ao copiar descrição: ', err);
                    alert('Falha ao copiar. Por favor, copie manualmente.');
                });
            }
        });
    }

    function showStatusMessage(element, message, type) {
        if (element) {
            element.textContent = message;
            element.className = 'status-message'; 
            element.classList.add(type); 
            element.style.display = 'block';
        }
    }

    function hideStatusMessage(element) {
        if (element) {
            element.style.display = 'none';
            element.textContent = '';
        }
    }
});