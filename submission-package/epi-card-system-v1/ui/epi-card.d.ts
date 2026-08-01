/**
 * Epi-Card Web Component contract v1.0.0.
 * The custom element is a projection of an approved engagement/rendition.
 * It never mutates semantic state directly; write requests are emitted for the host.
 */

export type QLPhase = "bimba" | "pratibimba";
export type QLAddress =
  | "P0" | "P1" | "P2" | "P3" | "P4" | "P5"
  | "P0′" | "P1′" | "P2′" | "P3′" | "P4′" | "P5′";
export type QLOccupancy =
  | "present" | "latent" | "missing" | "unknown"
  | "withheld" | "conflicted" | "overdetermined";
export type CardFace = "front" | "back";
export type CardPhaseView = "bimba" | "pratibimba" | "paired";
export type DisclosureProjection = "private" | "shared" | "public";

export interface AssetRef {
  id: string;
  sha256: string;
  mediaType: string;
  role: string;
  url?: string;
  packagePath?: string;
  width?: number;
  height?: number;
  durationMs?: number;
  alphaMode?: "none" | "straight" | "premultiplied";
}

export interface QLPositionView {
  id: string;
  address: QLAddress;
  phase: QLPhase;
  index: 0 | 1 | 2 | 3 | 4 | 5;
  canonicalUnit: string;
  canonicalQuestion: string;
  structuralRole: string;
  localLabel?: string;
  localQuestion?: string;
  shortSummary?: string;
  extendedArticulation?: string;
  occupancy: QLOccupancy;
  occupancyReason?: string;
  salience: number;
  sourceLinks: ReadonlyArray<{ id: string; label: string; href?: string }>;
  symbolState?: AssetRef;
  sceneRange?: { startFrame: number; durationFrames: number; fps: number };
  audioState?: AssetRef;
  nestedFrameUrl?: string;
  auditUrl?: string;
  okfUrl?: string;
}

export interface QLPairView {
  index: 0 | 1 | 2 | 3 | 4 | 5;
  bimba: QLPositionView;
  pratibimba: QLPositionView;
  reciprocalStatement: string;
  scenePreview?: AssetRef;
  audioPreview?: AssetRef;
}

export interface ReturnView {
  selfImplication: string;
  remainder: string;
  achievedWork?: string;
  nextGround: string;
  semanticDelta: Record<string, unknown>;
  mediaDelta: Record<string, unknown>;
  nextEngagementUrl?: string;
}

export interface EpiCardData {
  version: "1.0.0";
  engagementId: string;
  slug?: string;
  title: string;
  edition?: string;
  disclosure: DisclosureProjection;
  front: {
    poster: AssetRef;
    video?: AssetRef;
    loopVideo?: AssetRef;
    audio?: AssetRef;
    symbol: AssetRef;
    symbolRole: "overlay" | "cutout" | "alpha-mask" | "luma-mask" | "window" | "transition-matte" | "boundary";
    titleOutline?: AssetRef;
    captions?: AssetRef;
    description: string;
  };
  back: {
    symbol: AssetRef;
    pairs: readonly [QLPairView, QLPairView, QLPairView, QLPairView, QLPairView, QLPairView];
    return: ReturnView;
  };
  links: {
    self: string;
    fullObject?: string;
    okf?: string;
    printFront?: string;
    printBack?: string;
  };
}

export interface EpiCardState {
  face: CardFace;
  phase: CardPhaseView;
  activePosition: 0 | 1 | 2 | 3 | 4 | 5 | null;
  depth: number;
  playing: boolean;
  muted: boolean;
  volume: number;
  reducedMotion: boolean;
}

export interface EpiCardActionRequestDetail {
  action: string;
  engagementId: string;
  input: Record<string, unknown>;
  source: "front" | "hex-edge" | "pair-drawer" | "return" | "depth";
}

export interface EpiCardPositionChangeDetail {
  index: 0 | 1 | 2 | 3 | 4 | 5 | null;
  pair?: QLPairView;
  reason: "pointer" | "keyboard" | "programmatic" | "close";
}

export interface EpiCardViewChangeDetail {
  previous: EpiCardState;
  current: EpiCardState;
}

export interface EpiCardPlaybackDetail {
  playing: boolean;
  currentFrame: number;
  activeAddress?: QLAddress;
  activePair?: 0 | 1 | 2 | 3 | 4 | 5;
}

export interface EpiCardAssetErrorDetail {
  asset?: AssetRef;
  code: string;
  message: string;
  recoverable: boolean;
}

export interface EpiCardElement extends HTMLElement {
  /** URL returning EpiCardData JSON for the selected disclosure projection. */
  src: string;
  /** Optional data object. When set, it takes precedence over src until cleared. */
  data: EpiCardData | null;
  disclosure: DisclosureProjection;
  face: CardFace;
  phase: CardPhaseView;
  activePosition: 0 | 1 | 2 | 3 | 4 | 5 | null;
  muted: boolean;
  volume: number;
  reducedMotion: boolean;
  autoplay: boolean;
  preload: "none" | "metadata" | "poster" | "auto";
  readonly state: Readonly<EpiCardState>;
  readonly loaded: boolean;

  load(): Promise<void>;
  play(): Promise<void>;
  pause(): void;
  flip(face?: CardFace): void;
  setPhase(phase: CardPhaseView): void;
  openPair(index: 0 | 1 | 2 | 3 | 4 | 5): void;
  closePair(): void;
  openDepth(url: string): Promise<void>;
  backDepth(): void;
  seekToAddress(address: QLAddress): void;
  exportStill(): Promise<Blob>;
}

export type EpiCardEventMap = {
  "epi-card-ready": CustomEvent<{ data: EpiCardData }>;
  "epi-view-change": CustomEvent<EpiCardViewChangeDetail>;
  "epi-position-change": CustomEvent<EpiCardPositionChangeDetail>;
  "epi-play-state": CustomEvent<EpiCardPlaybackDetail>;
  "epi-action-request": CustomEvent<EpiCardActionRequestDetail>;
  "epi-relation-follow": CustomEvent<{ from: QLAddress; to: QLAddress | "P0+"; relation: string }>;
  "epi-asset-error": CustomEvent<EpiCardAssetErrorDetail>;
};

export interface EpiCardHTMLElementEventMap extends HTMLElementEventMap, EpiCardEventMap {}

declare global {
  interface HTMLElementTagNameMap {
    "epi-card": EpiCardElement;
  }
}

export {};
