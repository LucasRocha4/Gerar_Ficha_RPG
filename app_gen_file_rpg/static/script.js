const skillAttributeMap = {
    'acrobatics': 'dexterity',
    'animal-handling': 'wisdom',
    'arcana': 'intelligence',
    'athletics': 'strength',
    'deception': 'charisma',
    'history': 'intelligence',
    'insight': 'wisdom',
    'intimidation': 'charisma',
    'investigation': 'intelligence',
    'medicine': 'wisdom',
    'nature': 'intelligence',
    'perception': 'wisdom',
    'performance': 'charisma',
    'persuasion': 'charisma',
    'religion': 'intelligence',
    'sleight-of-hand': 'dexterity',
    'stealth': 'dexterity',
    'survival': 'wisdom'
};

const saveAttributeMap = {
    'strength-save': 'strength',
    'dexterity-save': 'dexterity',
    'constitution-save': 'constitution',
    'intelligence-save': 'intelligence',
    'wisdom-save': 'wisdom',
    'charisma-save': 'charisma'
};

function calculateModifier(score) {
    return Math.floor((score - 10) / 2);
}

function formatModifier(modifier) {
    return modifier >= 0 ? `+${modifier}` : `${modifier}`;
}

function updateAttributeModifier(attributeName) {
    const scoreInput = document.getElementById(attributeName);
    const modifierElement = document.getElementById(`${attributeName}-modifier`);
    
    if (scoreInput && modifierElement) {
        const score = parseInt(scoreInput.value) || 10;
        const modifier = calculateModifier(score);
        modifierElement.textContent = formatModifier(modifier);
        
        updateRelatedSkills(attributeName);
        updateRelatedSaves(attributeName);
        
        if (attributeName === 'dexterity') {
            updateInitiative();
        }
        
        if (attributeName === 'wisdom') {
            updatePassivePerception();
        }
    }
}

function updateRelatedSkills(attributeName) {
    Object.keys(skillAttributeMap).forEach(skillName => {
        if (skillAttributeMap[skillName] === attributeName) {
            updateSkillBonus(skillName);
        }
    });
}

function updateRelatedSaves(attributeName) {
    Object.keys(saveAttributeMap).forEach(saveName => {
        if (saveAttributeMap[saveName] === attributeName) {
            updateSaveBonus(saveName);
        }
    });
}

function updateSkillBonus(skillName) {
    const attributeName = skillAttributeMap[skillName];
    const attributeScore = parseInt(document.getElementById(attributeName)?.value) || 10;
    const attributeModifier = calculateModifier(attributeScore);
    
    const proficiencyCheckbox = document.getElementById(`${skillName}-prof`);
    const proficiencyBonus = parseInt(document.getElementById('proficiency-bonus')?.value) || 2;
    const skillBonusElement = document.getElementById(skillName);
    
    if (skillBonusElement) {
        let totalBonus = attributeModifier;
        
        if (proficiencyCheckbox && proficiencyCheckbox.checked) {
            totalBonus += proficiencyBonus;
        }
        
        skillBonusElement.textContent = formatModifier(totalBonus);
    }
}

function updateSaveBonus(saveName) {
    const attributeName = saveAttributeMap[saveName];
    const attributeScore = parseInt(document.getElementById(attributeName)?.value) || 10;
    const attributeModifier = calculateModifier(attributeScore);
    
    const proficiencyCheckbox = document.getElementById(`${saveName}-prof`);
    const proficiencyBonus = parseInt(document.getElementById('proficiency-bonus')?.value) || 2;
    const saveBonusElement = document.getElementById(saveName);
    
    if (saveBonusElement) {
        let totalBonus = attributeModifier;
        
        if (proficiencyCheckbox && proficiencyCheckbox.checked) {
            totalBonus += proficiencyBonus;
        }
        
        saveBonusElement.textContent = formatModifier(totalBonus);
    }
}

function updateInitiative() {
    const dexterityScore = parseInt(document.getElementById('dexterity')?.value) || 10;
    const dexterityModifier = calculateModifier(dexterityScore);
    const initiativeElement = document.getElementById('initiative');
    
    if (initiativeElement) {
        initiativeElement.textContent = formatModifier(dexterityModifier);
    }
}

function updatePassivePerception() {
    const wisdomScore = parseInt(document.getElementById('wisdom')?.value) || 10;
    const wisdomModifier = calculateModifier(wisdomScore);
    const proficiencyCheckbox = document.getElementById('perception-prof');
    const proficiencyBonus = parseInt(document.getElementById('proficiency-bonus')?.value) || 2;
    const passivePerceptionElement = document.getElementById('passive-perception');
    
    if (passivePerceptionElement) {
        let passiveValue = 10 + wisdomModifier;
        
        if (proficiencyCheckbox && proficiencyCheckbox.checked) {
            passiveValue += proficiencyBonus;
        }
        
        passivePerceptionElement.textContent = passiveValue;
    }
}

function updateAllSkills() {
    Object.keys(skillAttributeMap).forEach(skillName => {
        updateSkillBonus(skillName);
    });
}

function updateAllSaves() {
    Object.keys(saveAttributeMap).forEach(saveName => {
        updateSaveBonus(saveName);
    });
}

function updateAllAttributeModifiers() {
    const attributes = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'];
    attributes.forEach(attr => {
        updateAttributeModifier(attr);
    });
}

function updateProficiencyBonus() {
    updateAllSkills();
    updateAllSaves();
    updatePassivePerception();
}

function addEventListeners() {
    const attributes = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'];
    attributes.forEach(attr => {
        const input = document.getElementById(attr);
        if (input) {
            input.addEventListener('input', () => updateAttributeModifier(attr));
            input.addEventListener('change', () => updateAttributeModifier(attr));
        }
    });
    
    const proficiencyBonusInput = document.getElementById('proficiency-bonus');
    if (proficiencyBonusInput) {
        proficiencyBonusInput.addEventListener('input', updateProficiencyBonus);
        proficiencyBonusInput.addEventListener('change', updateProficiencyBonus);
    }
    
    Object.keys(skillAttributeMap).forEach(skillName => {
        const checkbox = document.getElementById(`${skillName}-prof`);
        if (checkbox) {
            checkbox.addEventListener('change', () => {
                updateSkillBonus(skillName);
                if (skillName === 'perception') {
                    updatePassivePerception();
                }
            });
        }
    });
    
    Object.keys(saveAttributeMap).forEach(saveName => {
        const checkbox = document.getElementById(`${saveName}-prof`);
        if (checkbox) {
            checkbox.addEventListener('change', () => updateSaveBonus(saveName));
        }
    });
}

function validateAttributeInput(input) {
    let value = parseInt(input.value);
    
    if (isNaN(value) || value < 1) {
        value = 1;
    } else if (value > 30) {
        value = 30;
    }
    
    input.value = value;
}

function addAttributeValidation() {
    const attributes = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'];
    attributes.forEach(attr => {
        const input = document.getElementById(attr);
        if (input) {
            input.addEventListener('blur', () => validateAttributeInput(input));
        }
    });
}

function validateProficiencyBonus(input) {
    let value = parseInt(input.value);
    
    if (isNaN(value) || value < 2) {
        value = 2;
    } else if (value > 6) {
        value = 6;
    }
    
    input.value = value;
}

function addProficiencyValidation() {
    const proficiencyBonusInput = document.getElementById('proficiency-bonus');
    if (proficiencyBonusInput) {
        proficiencyBonusInput.addEventListener('blur', () => validateProficiencyBonus(proficiencyBonusInput));
    }
}

function saveCharacterData() {
    const characterData = {};
    
    const basicFields = [
        'character-name', 'class-level', 'background', 'player-name',
        'race', 'alignment', 'experience'
    ];
    
    basicFields.forEach(fieldId => {
        const element = document.getElementById(fieldId);
        if (element) {
            characterData[fieldId] = element.value;
        }
    });
    
    const attributes = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'];
    attributes.forEach(attr => {
        const element = document.getElementById(attr);
        if (element) {
            characterData[attr] = element.value;
        }
    });
    
    const proficiencyBonus = document.getElementById('proficiency-bonus');
    if (proficiencyBonus) {
        characterData['proficiency-bonus'] = proficiencyBonus.value;
    }
    
    Object.keys(skillAttributeMap).forEach(skillName => {
        const checkbox = document.getElementById(`${skillName}-prof`);
        if (checkbox) {
            characterData[`${skillName}-prof`] = checkbox.checked;
        }
    });
    
    Object.keys(saveAttributeMap).forEach(saveName => {
        const checkbox = document.getElementById(`${saveName}-prof`);
        if (checkbox) {
            characterData[`${saveName}-prof`] = checkbox.checked;
        }
    });
    
    localStorage.setItem('dnd-character-data', JSON.stringify(characterData));
}

function loadCharacterData() {
    const savedData = localStorage.getItem('dnd-character-data');
    if (savedData) {
        try {
            const characterData = JSON.parse(savedData);
            
            Object.keys(characterData).forEach(fieldId => {
                const element = document.getElementById(fieldId);
                if (element) {
                    if (element.type === 'checkbox') {
                        element.checked = characterData[fieldId];
                    } else {
                        element.value = characterData[fieldId];
                    }
                }
            });
            
            updateAllAttributeModifiers();
            updateProficiencyBonus();
        } catch (error) {
            console.error('Erro ao carregar dados do personagem:', error);
        }
    }
}

function addAutoSave() {
    setInterval(saveCharacterData, 30000);
    
    window.addEventListener('beforeunload', saveCharacterData);
}

function initializeCharacterSheet() {
    addEventListeners();
    
    addAttributeValidation();
    addProficiencyValidation();
    
    updateAllAttributeModifiers();
    updateProficiencyBonus();
    
    loadCharacterData();
    
    addAutoSave();
    
    console.log('Ficha de personagem D&D 5e inicializada com sucesso!');
}

document.addEventListener('DOMContentLoaded', initializeCharacterSheet);

function debugCharacterSheet() {
    console.log('=== DEBUG DA FICHA DE PERSONAGEM ===');
    
    const attributes = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'];
    attributes.forEach(attr => {
        const score = document.getElementById(attr)?.value;
        const modifier = document.getElementById(`${attr}-modifier`)?.textContent;
        console.log(`${attr}: ${score} (${modifier})`);
    });
    
    console.log('Bônus de Proficiência:', document.getElementById('proficiency-bonus')?.value);
    console.log('Iniciativa:', document.getElementById('initiative')?.textContent);
    console.log('Percepção Passiva:', document.getElementById('passive-perception')?.textContent);
    
    console.log('=== FIM DO DEBUG ===');
}

window.debugCharacterSheet = debugCharacterSheet;

