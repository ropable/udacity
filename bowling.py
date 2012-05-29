'''
UNIT 1: Bowling:

You will write the function bowling(balls), which returns an integer indicating
the score of a ten-pin bowling game.  balls is a list of integers indicating
how many pins are knocked down with each ball.  For example, a perfect game of
bowling would be described with:

    >>> bowling([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
    300

The rules of bowling are as follows:

(1) A game consists of 10 frames. In each frame you roll one or two balls,
except for the tenth frame, where you roll one, two, or three.  Your total
score is the sum of your scores for the ten frames.
(2) If you knock down fewer than ten pins with your two balls in the frame,
you score the total knocked down.  For example, bowling([8, 1, 7, ...]) means
that you knocked down a total of 9 pins in the first frame.  You score 9 point
for the frame, and you used up two balls in the frame. The second frame will
start with the 7.
(3) If you knock down all ten pins on your second ball it is called a 'spare'
and you score 10 points plus a bonus: whatever you roll with your next ball.
The next ball will also count in the next frame, so the next ball counts twice
(except in the tenth frame, in which case the bonus ball counts only once).
For example, bowling([8, 2, 7, ...]) means you get a spare in the first frame.
You score 10 + 7 for the frame; the second frame starts with the 7.
(4) If you knock down all ten pins on your first ball it is called a 'strike'
and you score 10 points plus a bonus of your score on the next two balls.
(The next two balls also count in the next frame, except in the tenth frame.)
For example, bowling([10, 7, 3, ...]) means that you get a strike, you score
10 + 7 + 3 = 20 in the first frame; the second frame starts with the 7.
'''

def bowling(balls):
    "Compute the total score for a player's game of bowling."
    score = 0
    frames = []
    for i in range(9):
        pins1 = balls.pop(0)
        if pins1 == 10:
            frames.append(pins1)
            continue
        else:
            pins2 = balls.pop(0)
            frames.append((pins1, pins2))
    # Last frame.
    if len(balls) == 1:
        frames.append(balls.pop(0))
    elif len(balls) == 2:
        frames.append((balls.pop(0), balls.pop(0)))
    else:
        frames.append((balls.pop(0), balls.pop(0), balls.pop(0)))
    count = 0
    for i, f in enumerate(frames):
        count += 1
        if i == 9: # Last frame is always a tuple; just sum it.
            score += sum(f)
        else: # Handle frames 1-9.
            if f == 10: # Strike!
                # Obtain the total of the next two balls.
                score += 10
                # Handle frame nine. Frame ten will always be a tuple.
                if i == 8: # Frame 9
                    score += (frames[9][0] + frames[9][1])
                # Handle other frames.
                elif frames[i+1] == 10: # Next ball was a strike, too!
                    score += 10
                    if isinstance(frames[i+2], tuple): # Didn't quite manage a Turkey.
                        score += frames[i+2][0] # First ball of next frame.
                    else: # Damn! A Turkey!!!
                        score += 10
                else: # Next ball wasn't a strike.
                    score += sum(frames[i+1])
            elif sum(f) == 10: # Spare!
                score += 10
                if i == 8: # Frame 9
                    score += frames[9][0] # First element of the tuple.
                elif frames[i+1] == 10: # Next ball was a strike, too!
                    score += 10
                else:
                    score += frames[i+1][0] # First ball of next frame.
            else: # Not a strike or spare.
                score += sum(f)
        #print('Frame {0}: {1} total: {2}'.format(count, f, score))
    return score

def test_bowling():
    assert   0 == bowling([0] * 20)
    assert  20 == bowling([1] * 20)
    assert  80 == bowling([4] * 20)
    assert 190 == bowling([9,1] * 10 + [9])
    assert 300 == bowling([10] * 12)
    assert 200 == bowling([10, 5,5] * 5 + [10])
    assert  11 == bowling([0,0] * 9 + [10,1,0])
    assert  12 == bowling([0,0] * 8 + [10, 1,0])
    print('Tests pass')

test_bowling()