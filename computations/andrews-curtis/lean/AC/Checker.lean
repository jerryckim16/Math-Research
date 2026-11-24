import AC.Defs

/-!
# A certificate checker for AC moves, and its soundness

`check p ms q = true → ACEquiv p q` (`check_sound`).  The checker mirrors the
move semantics of `computations/andrews-curtis/ac_check.py`:

* `invert i`    r_i ← r_i⁻¹
* `mul i e`     r_i ← r_i r_j^e (j the other index, e = +1 for `true`)
* `conj i g`    r_i ← g r_i g⁻¹ (g a letter)
* `cycle i k`   r_i = uv ↦ u⁻¹(uv)u = vu, u the first (k mod |r_i|) letters

each followed by free reduction `red`.  Every move is justified by one
`ACStep` (`cycle` by a conjugation) followed by a `free` step, using
`freeEq_red : FreeEq w (red w)`.
-/

namespace AC

/-! ## Basic lemmas on words -/

theorem winv_nil : winv [] = [] := rfl

theorem winv_append (u v : Word) : winv (u ++ v) = winv v ++ winv u := by
  simp [winv, List.map_append, List.reverse_append]

theorem winv_cons (a : L) (w : Word) : winv (a :: w) = winv w ++ [a.inv] := by
  simp [winv]

theorem winv_winv (w : Word) : winv (winv w) = w := by
  induction w with
  | nil => rfl
  | cons a w ih => rw [winv_cons, winv_append, ih]; simp [winv]

/-! ## Free equality -/

theorem FreeEq.append_left (p : Word) {u v : Word} (h : FreeEq u v) :
    FreeEq (p ++ u) (p ++ v) := by
  induction h with
  | refl w => exact .refl _
  | cancel q r a =>
    have h := FreeEq.cancel (p ++ q) r a
    simpa [List.append_assoc] using h
  | symm _ ih => exact .symm ih
  | trans _ _ ih1 ih2 => exact .trans ih1 ih2

theorem FreeEq.append_right (q : Word) {u v : Word} (h : FreeEq u v) :
    FreeEq (u ++ q) (v ++ q) := by
  induction h with
  | refl w => exact .refl _
  | cancel p r a =>
    have h := FreeEq.cancel p (r ++ q) a
    simpa [List.append_assoc] using h
  | symm _ ih => exact .symm ih
  | trans _ _ ih1 ih2 => exact .trans ih1 ih2

/-- `p u u⁻¹ q ~ p q`. -/
theorem FreeEq.cancel_word (u : Word) : ∀ (p q : Word),
    FreeEq (p ++ u ++ winv u ++ q) (p ++ q) := by
  induction u with
  | nil => intro p q; simpa [winv] using FreeEq.refl (p ++ q)
  | cons c u ih =>
    intro p q
    have h1 := ih (p ++ [c]) (c.inv :: q)
    have h2 := FreeEq.cancel p q c
    have e : p ++ c :: u ++ winv (c :: u) ++ q = p ++ [c] ++ u ++ winv u ++ c.inv :: q := by
      simp [winv_cons, List.append_assoc]
    have e2 : p ++ [c] ++ c.inv :: q = p ++ c :: c.inv :: q := by simp
    rw [e]; rw [e2] at h1
    exact .trans h1 h2

/-! ## Free reduction -/

/-- `cancels a b` iff `b = a⁻¹`. -/
def cancels : L → L → Bool
  | .x, .X => true
  | .X, .x => true
  | .y, .Y => true
  | .Y, .y => true
  | _, _ => false

theorem cancels_spec {a b : L} (h : cancels a b = true) : b = a.inv := by
  cases a <;> cases b <;> first | rfl | exact absurd h (by decide)

/-- Push a letter onto a reduced word (stack-style free reduction). -/
def push (a : L) : Word → Word
  | [] => [a]
  | b :: t =>
    match cancels a b with
    | true => t
    | false => a :: b :: t

/-- Free reduction. -/
def red (w : Word) : Word := w.foldr push []

theorem freeEq_push (a : L) (w : Word) : FreeEq (a :: w) (push a w) := by
  cases w with
  | nil => exact .refl _
  | cons b t =>
    cases h : cancels a b with
    | true =>
      have e : push a (b :: t) = t := by simp [push, h]
      rw [e]
      have hb := cancels_spec h; subst hb
      exact FreeEq.cancel [] t a
    | false =>
      have e : push a (b :: t) = a :: b :: t := by simp [push, h]
      rw [e]; exact .refl _

theorem freeEq_red (w : Word) : FreeEq w (red w) := by
  induction w with
  | nil => exact .refl _
  | cons a w ih =>
    show FreeEq (a :: w) (push a (red w))
    exact .trans (FreeEq.append_left [a] ih) (freeEq_push a (red w))

/-! ## Reflexive–transitive closure -/

theorem Star.single {α : Type} {R : α → α → Prop} {a b : α} (h : R a b) : Star R a b :=
  .tail (.refl a) h

theorem Star.trans {α : Type} {R : α → α → Prop} {a b c : α}
    (h1 : Star R a b) (h2 : Star R b c) : Star R a c := by
  induction h2 with
  | refl => exact h1
  | tail _ h ih => exact .tail ih h

theorem ACEquiv.refl (p : Pres) : ACEquiv p p := Star.refl p
theorem ACEquiv.trans {p q r : Pres} (h1 : ACEquiv p q) (h2 : ACEquiv q r) : ACEquiv p r :=
  Star.trans h1 h2
theorem ACEquiv.single {p q : Pres} (h : ACStep p q) : ACEquiv p q := Star.single h

/-! ## Symmetry: every AC move is undone by AC moves -/

theorem freeEq_mul_pw (a b : Word) (e : Bool) : FreeEq (a ++ pw b e ++ pw b !e) a := by
  cases e
  · have h := FreeEq.cancel_word (winv b) a []
    rw [winv_winv] at h; simpa [pw] using h
  · have h := FreeEq.cancel_word b a []
    simpa [pw] using h

theorem freeEq_conj (a w : Word) : FreeEq (winv w ++ (w ++ a ++ winv w) ++ winv (winv w)) a := by
  rw [winv_winv]
  have h1 := FreeEq.cancel_word (winv w) [] (a ++ winv w ++ w)
  rw [winv_winv] at h1
  have h2 := FreeEq.cancel_word (winv w) a []
  rw [winv_winv] at h2
  simp only [List.nil_append, List.append_nil, List.append_assoc] at h1 h2 ⊢
  exact .trans h1 h2

theorem ACStep.reverse {p q : Pres} (h : ACStep p q) : ACEquiv q p := by
  cases h with
  | inv₀ a b =>
    have s := ACStep.inv₀ (winv a) b; rw [winv_winv] at s; exact .single s
  | inv₁ a b =>
    have s := ACStep.inv₁ a (winv b); rw [winv_winv] at s; exact .single s
  | mul₀ a b e =>
    exact .trans (.single (ACStep.mul₀ (a ++ pw b e) b (!e)))
      (.single (ACStep.free₀ b (freeEq_mul_pw a b e)))
  | mul₁ a b e =>
    exact .trans (.single (ACStep.mul₁ a (b ++ pw a e) (!e)))
      (.single (ACStep.free₁ a (freeEq_mul_pw b a e)))
  | conj₀ a b w =>
    exact .trans (.single (ACStep.conj₀ (w ++ a ++ winv w) b (winv w)))
      (.single (ACStep.free₀ b (freeEq_conj a w)))
  | conj₁ a b w =>
    exact .trans (.single (ACStep.conj₁ a (w ++ b ++ winv w) (winv w)))
      (.single (ACStep.free₁ a (freeEq_conj b w)))
  | free₀ b h => exact .single (ACStep.free₀ b (.symm h))
  | free₁ a h => exact .single (ACStep.free₁ a (.symm h))

theorem ACEquiv.symm {p q : Pres} (h : ACEquiv p q) : ACEquiv q p := by
  induction h with
  | refl => exact .refl _
  | tail _ s ih => exact ACEquiv.trans s.reverse ih

/-! ## The checker -/

/-- Relator index, as in the JSON certificates: `r0` = index 0, `r1` = index 1. -/
inductive Idx where
  | r0 | r1
  deriving DecidableEq, Repr

/-- Elementary moves of the JSON certificates. -/
inductive Move where
  | invert (i : Idx)
  | mul (i : Idx) (e : Bool)
  | conj (i : Idx) (g : L)
  | cycle (i : Idx) (k : Nat)
  deriving Repr

def Move.idx : Move → Idx
  | .invert i => i
  | .mul i _ => i
  | .conj i _ => i
  | .cycle i _ => i

/-- New value of the acted-on relator `a`, given the other relator `b`. -/
def act : Move → Word → Word → Word
  | .invert _, a, _ => red (winv a)
  | .mul _ e, a, b => red (a ++ pw b e)
  | .conj _ g, a, _ => red ([g] ++ a ++ winv [g])
  | .cycle _ k, a, _ =>
    let u := a.take (k % a.length)
    red (winv u ++ a ++ winv (winv u))

def apply (p : Pres) (m : Move) : Pres :=
  match m.idx with
  | .r0 => (act m p.1 p.2, p.2)
  | .r1 => (p.1, act m p.2 p.1)

def run (p : Pres) (ms : List Move) : Pres := ms.foldl apply p

def check (p : Pres) (ms : List Move) (q : Pres) : Bool := decide (run p ms = q)

/-! ## Soundness -/

theorem act_sound₀ (m : Move) (a b : Word) : ACEquiv (a, b) (act m a b, b) := by
  cases m with
  | invert i => exact .trans (.single (.inv₀ a b)) (.single (.free₀ b (freeEq_red _)))
  | mul i e => exact .trans (.single (.mul₀ a b e)) (.single (.free₀ b (freeEq_red _)))
  | conj i g => exact .trans (.single (.conj₀ a b [g])) (.single (.free₀ b (freeEq_red _)))
  | cycle i k =>
    exact .trans (.single (.conj₀ a b (winv (a.take (k % a.length)))))
      (.single (.free₀ b (freeEq_red _)))

theorem act_sound₁ (m : Move) (a b : Word) : ACEquiv (b, a) (b, act m a b) := by
  cases m with
  | invert i => exact .trans (.single (.inv₁ b a)) (.single (.free₁ b (freeEq_red _)))
  | mul i e => exact .trans (.single (.mul₁ b a e)) (.single (.free₁ b (freeEq_red _)))
  | conj i g => exact .trans (.single (.conj₁ b a [g])) (.single (.free₁ b (freeEq_red _)))
  | cycle i k =>
    exact .trans (.single (.conj₁ b a (winv (a.take (k % a.length)))))
      (.single (.free₁ b (freeEq_red _)))

theorem apply_sound (p : Pres) (m : Move) : ACEquiv p (apply p m) := by
  obtain ⟨a, b⟩ := p
  unfold apply
  cases m.idx with
  | r0 => exact act_sound₀ m a b
  | r1 => exact act_sound₁ m b a

theorem run_sound (ms : List Move) : ∀ p : Pres, ACEquiv p (run p ms) := by
  induction ms with
  | nil => intro p; exact .refl p
  | cons m ms ih => intro p; exact .trans (apply_sound p m) (ih (apply p m))

/-- **Soundness of the checker.** -/
theorem check_sound {p q : Pres} {ms : List Move} (h : check p ms q = true) :
    ACEquiv p q := by
  have e : run p ms = q := of_decide_eq_true h
  exact e ▸ run_sound ms p

end AC
