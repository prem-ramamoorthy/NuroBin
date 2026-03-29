document.addEventListener('DOMContentLoaded', async () => {
    const memoryContainer = document.getElementById('memoryContainer');

    async function loadMemoryTriggers() {
        try {
            const triggers = await ApiClient.getMemoryTriggers();
            
            if (!triggers || triggers.length === 0) {
                memoryContainer.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">💭</div>
                        <h3>Not many memories yet?</h3>
                        <p class="text-muted">No memory triggers have been added yet. Your caregivers can add them for you.</p>
                    </div>`;
                return;
            }

            memoryContainer.innerHTML = '';
            triggers.forEach(fm => {
                const card = document.createElement('div');
                card.className = 'glass-card memory-card fade-in';
                
                const photoHtml = fm.photo_url 
                    ? `<img src="${fm.photo_url}" alt="${fm.name}">` 
                    : `<span class="placeholder-icon">👤</span>`;

                card.innerHTML = `
                    <div class="memory-photo">
                        ${photoHtml}
                    </div>
                    <div class="memory-info">
                        <span class="memory-relation">${fm.relation || 'Relation'}</span>
                        <h3 class="memory-name">${fm.name || 'Unknown Person'}</h3>
                        <div class="memory-note">
                            ${fm.notes || 'No specific memory triggers for this person.'}
                        </div>
                    </div>
                `;
                memoryContainer.appendChild(card);
            });

        } catch (error) {
            console.error('Failed to load memory triggers:', error);
            ApiClient.notify('Error loading memories', 'error');
        }
    }

    loadMemoryTriggers();
});
