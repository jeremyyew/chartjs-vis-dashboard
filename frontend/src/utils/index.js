import Const from '@/components/Const';

function indexOfMax(arr) {
  if (arr.length === 0) {
    return -1;
  }

  let max = arr[0];
  let maxIndex = 0;

  for (let i = 1; i < arr.length; i += 1) {
    if (arr[i] > max) {
      maxIndex = i;
      max = arr[i];
    }
  }

  return maxIndex;
}

function chooseColorScheme(len) {
  switch (len) {
    case 2:
      return Const.colorScheme2;
    case 3:
      return Const.colorScheme3;
    case 4:
      return Const.colorScheme3;
    case 5:
      return Const.colorScheme5;
    case 6:
      return Const.colorScheme6;
    case 7:
      return Const.colorScheme7;
    case 8:
      return Const.colorScheme8;
    case 9:
      return Const.colorScheme9;
    default:
      return Const.colorScheme10;
  }
}

const labelUtil = label => ({
  ...Const.scaleLabelConfig,
  labelString: label,
});

export default {
  indexOfMax,
  chooseColorScheme,
  labelUtil,
};
