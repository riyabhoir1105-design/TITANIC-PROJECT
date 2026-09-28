const form = document.getElementById('predictionForm');
const resultBox = document.getElementById('resultBox');
const resultText = document.getElementById('resultText');

const passengerClass = document.getElementById('passengerClass');
const ageInput = document.getElementById('age');
const siblingsInput = document.getElementById('siblings');
const parentsChildrenInput = document.getElementById('parentsChildren');
const fareInput = document.getElementById('fare');
const familySizeInput = document.getElementById('familySize');
const isAloneInput = document.getElementById('isAlone');
const genderInput = document.getElementById('gender');
const embarkedInput = document.getElementById('embarked');

function syncFamilySize() {
  const siblings = Number(siblingsInput.value || 0);
  const parentsChildren = Number(parentsChildrenInput.value || 0);
  const autoFamilySize = siblings + parentsChildren + 1;
  familySizeInput.value = autoFamilySize;
}

siblingsInput.addEventListener('input', syncFamilySize);
parentsChildrenInput.addEventListener('input', syncFamilySize);

familySizeInput.addEventListener('input', () => {
  const value = Number(familySizeInput.value || 0);
  isAloneInput.checked = value <= 1;
});

isAloneInput.addEventListener('change', () => {
  if (isAloneInput.checked) {
    familySizeInput.value = 1;
  }
});

function predictSurvival() {
  const pclass = Number(passengerClass.value);
  const age = Number(ageInput.value || 0);
  const siblings = Number(siblingsInput.value || 0);
  const parentsChildren = Number(parentsChildrenInput.value || 0);
  const fare = Number(fareInput.value || 0);
  const familySize = Number(familySizeInput.value || 1);
  const isAlone = isAloneInput.checked || familySize <= 1;
  const gender = genderInput.value;
  const embarked = embarkedInput.value;

  let score = 0;

  if (gender === 'female') {
    score += 2.6;
  } else {
    score -= 1.2;
  }

  if (pclass === 1) {
    score += 1.6;
  } else if (pclass === 2) {
    score += 0.7;
  } else {
    score -= 1.3;
  }

  if (age > 0 && age < 18) {
    score += 1.1;
  } else if (age > 50) {
    score -= 0.5;
  }

  if (fare > 50) {
    score += 1.1;
  } else if (fare > 20) {
    score += 0.5;
  }

  const totalRelatives = siblings + parentsChildren;
  if (totalRelatives > 0 && totalRelatives <= 3) {
    score += 0.8;
  }

  if (isAlone) {
    score -= 0.8;
  }

  if (embarked === 'C' || embarked === 'Q') {
    score += 0.5;
  } else if (embarked === 'S') {
    score -= 0.2;
  }

  const survived = score >= 1.2;

  return survived;
}

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const survived = predictSurvival();

  if (survived) {
    resultBox.className = 'result-box success';
    resultText.textContent = 'Passenger Survived';
  } else {
    resultBox.className = 'result-box danger';
    resultText.textContent = 'Passenger Did not Survive';
  }
});

syncFamilySize();
