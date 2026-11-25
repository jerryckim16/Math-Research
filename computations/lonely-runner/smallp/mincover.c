/* mincover.c -- covering number tau_k(p) (Allikvere, arXiv:2609.02604v2, Sec. 4):
 * least number of folded speed classes (1..h, h=(p-1)/2) covering every folded
 * time class 1..h, where v covers a iff (k+1)*d_p(a v) < p.
 * Unit symmetry: v covers a iff uv covers u^{-1}a, so some minimum cover
 * contains class 1 (scale by the inverse of any of its classes).
 * Exhaustive DFS for "a cover of size <= s containing 1": branch on an
 * uncovered time with fewest allowed coverers (every cover contains one of
 * them; earlier siblings excluded -- every cover is reached through the
 * first of its classes among the candidates), cut when the s-|L| largest
 * gains |cov(c) & U| over allowed c sum to < |U| (any completion adds at most
 * s-|L| classes, each covering at most its gain).  So "none" is exhaustive.
 * Usage: mincover k p      prints "p tau nodes cover..." ; stops at first s.
 *        mincover k p enum s   prints every MINIMAL cover C with 1 in C and
 *        |C| <= s (each exactly once: the uniqueness argument of covergen.c's
 *        header -- follow the first candidate lying in C), one per line.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define MAXW 4
typedef struct { uint64_t w[MAXW]; } bs;
static int k, p, h, W, S;
static bs cov[256];
static int L[64], nL, best[64];
static unsigned long long nodes;
static int pc(const bs *a){int s=0;for(int i=0;i<W;i++)s+=__builtin_popcountll(a->w[i]);return s;}
static int pa(const bs *a,const bs *b){int s=0;for(int i=0;i<W;i++)s+=__builtin_popcountll(a->w[i]&b->w[i]);return s;}
static int has(const bs *a,int x){return (a->w[x>>6]>>(x&63))&1;}
static int enumerate = 0;
static int minimal(void){ for(int i=0;i<nL;i++){ bs P=cov[L[i]]; for(int j=0;j<nL;j++) if(j!=i) for(int w=0;w<W;w++) P.w[w]&=~cov[L[j]].w[w]; if(!pc(&P)) return 0;} return 1; }
static int dfs(const bs *U, const bs *A) {
    nodes++;
    int nu = pc(U);
    if (!nu) { memcpy(best, L, sizeof(int)*nL);
        if (enumerate) { if (minimal()) { for(int i=0;i<nL;i++) printf(i?" %d":"%d",L[i]); printf("\n"); } return 0; }
        return 1; }
    int left = S - nL; if (left <= 0) return 0;
    int hist[256]; memset(hist,0,sizeof hist); int mx=0;
    for (int c=1;c<=h;c++) if (has(A,c)) { int g=pa(&cov[c],U); hist[g]++; if(g>mx)mx=g; }
    long got=0; int r=left; for(int g=mx;g>0&&r>0;g--){int t=hist[g]<r?hist[g]:r; got+=(long)t*g; r-=t;}
    if (got < nu) return 0;
    int besta=-1, bc=1<<30;
    for (int a=1;a<=h;a++) if (has(U,a)) { int c=0; for(int v=1;v<=h;v++) if(has(A,v)&&has(&cov[v],a)) c++; if(c<bc){bc=c;besta=a;} }
    if (bc==0) return 0;
    bs A2=*A;
    for (int v=1;v<=h;v++) if (has(&A2,v)&&has(&cov[v],besta)) {
        bs U2; for(int i=0;i<W;i++) U2.w[i]=U->w[i]&~cov[v].w[i];
        A2.w[v>>6]&=~(1ULL<<(v&63));
        L[nL++]=v; if (dfs(&U2,&A2)) return 1; nL--;
    }
    return 0;
}
int main(int argc,char**argv){
    k=atoi(argv[1]); p=atoi(argv[2]); h=(p-1)/2; W=(h+1+63)/64;
    for(int v=1;v<=h;v++){memset(&cov[v],0,sizeof(bs)); for(int a=1;a<=h;a++){int r=(a*v)%p; int d=r<p-r?r:p-r; if((k+1)*d<p) cov[v].w[a>>6]|=1ULL<<(a&63);} }
    int m=pc(&cov[1]);
    if (argc>4) { enumerate=1; S=atoi(argv[4]);
        bs U,A; memset(&U,0,sizeof U); memset(&A,0,sizeof A);
        for(int a=1;a<=h;a++){U.w[a>>6]|=1ULL<<(a&63); A.w[a>>6]|=1ULL<<(a&63);}
        for(int i=0;i<W;i++) U.w[i]&=~cov[1].w[i];
        A.w[0]&=~2ULL; nL=1; L[0]=1; nodes=0; dfs(&U,&A);
        fprintf(stderr,"enum p=%d s<=%d nodes=%llu\n",p,S,nodes); return 0; }
    for (S=(h+m-1)/m;;S++) {
        bs U,A; memset(&U,0,sizeof U); memset(&A,0,sizeof A);
        for(int a=1;a<=h;a++){U.w[a>>6]|=1ULL<<(a&63); A.w[a>>6]|=1ULL<<(a&63);}
        for(int i=0;i<W;i++) U.w[i]&=~cov[1].w[i];
        A.w[0]&=~2ULL; nL=1; L[0]=1; nodes=0;
        int ok=dfs(&U,&A);
        fprintf(stderr,"p=%d s=%d %s nodes=%llu\n",p,S,ok?"found":"none",nodes);
        if (ok) { /* verify */
            bs C; memset(&C,0,sizeof C); for(int i=0;i<S&&best[i];i++) for(int j=0;j<W;j++) C.w[j]|=cov[best[i]].w[j];
            int n=0; for(int i=0;i<S;i++) if(best[i]) n++;
            if (pc(&C)!=h) { fprintf(stderr,"VERIFY FAIL\n"); return 1; }
            printf("%d %d %llu",p,n,nodes); for(int i=0;i<n;i++) printf(" %d",best[i]); printf("\n"); return 0; }
    }
}
